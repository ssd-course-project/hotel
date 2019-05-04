from datetime import datetime

from django import forms
from django.http import Http404
from django.shortcuts import render
from django.views import generic

from analytics.models import RoomBooking
from clients.models import Client
from hotel.forms import RoomBookingForm
from .models import Room


class RoomListView(generic.ListView):
    model = Room
    template_name = "hotel/room_list.html"
    context_object_name = 'rooms'


class RoomSearchView(generic.ListView):
    model = Room
    template_name = "hotel/room_search.html"
    context_object_name = 'rooms'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        if not all((check_in, check_out)):
            error_message = "" \
                "Введите дату заезда и выезда, чтобы мы могли показать Вам " \
                "доступные в это время номера"
            context['error_message'] = error_message
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.GET:
            return queryset

        # TODO: validate check_in/checkout date
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        visitors = self.request.GET.get('visitors')
        price = self.request.GET.get('price')

        if all((check_in, check_out)):
            check_in = datetime.strptime(check_in, "%d.%m.%Y").date()
            check_out = datetime.strptime(check_out, "%d.%m.%Y").date()

            available_rooms = [
                room.id for room in queryset
                if room.room_status(check_in, check_out) ==
                   room.AVAILABLE_STATUS
            ]

            queryset = queryset.filter(id__in=available_rooms)

        if visitors:
            queryset = queryset.filter(sleeps_number=visitors)

        if price:
            queryset = queryset.filter(price__lte=price)

        return queryset


class RoomDetailView(generic.DetailView):
    model = Room
    context_object_name = 'room'


class RoomBookingView(generic.FormView):
    template_name = 'hotel/room_booking.html'
    success_url = '/'
    form_class = RoomBookingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self._get_room()
        return context

    def form_valid(self, form):
        room = self._get_room()
        check_in_date = form.cleaned_data.get('check_in_date')
        check_out_date = form.cleaned_data.get('check_out_date')

        room_status = room.room_status(check_in_date, check_out_date)
        if room_status != room.AVAILABLE_STATUS:
            error_message = "" \
                "К сожалению, в выбранный период все номера этого типа " \
                "забронированы. Попробуйте поменять даты "
            data = {"error_message": error_message}
            return render(
                self.request,
                self.template_name,
                context={**self.get_context_data(), **data}
            )

        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            raise forms.ValidationError("You are not our client!")

        RoomBooking.objects.create(
            room=room,
            renter=client,
            check_in_date=check_in_date,
            check_out_date=check_out_date
        )

        return super().form_valid(form)

    def _get_room(self):
        try:
            return Room.objects.get(id=self.kwargs.get('pk'))
        except Room.DoesNotExist:
            raise Http404


def about(request):
    return render(request, 'general/about.html')


def contacts(request):
    return render(request, 'general/contacts.html')


def components(request):
    return render(request, 'general/components.html')
