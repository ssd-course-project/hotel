from django import forms
from django.db.models import Q
from django.forms.models import modelform_factory
from django.http import Http404
from django.shortcuts import render
from django.views import generic

from analytics.models import RoomBooking
from clients.models import Client
from hotel.forms import RoomBookingForm
from .models import Room

from datetime import datetime


class RoomListView(generic.ListView):
    model = Room
    template_name = "hotel/room_list.html"
    context_object_name = 'rooms'


class RoomSearchView(generic.ListView):
    model = Room
    template_name = "hotel/room_search.html"
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = super().get_queryset()

        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        visitors = self.request.GET.get('visitors')
        price = self.request.GET.get('price')

        if check_in:
            check_in = datetime.strptime(check_in, "%d.%m.%Y").date()
            queryset = queryset.filter(
                Q(check_out_date__lte=check_in) |
                Q(check_out_date__isnull=True)
            )

        if check_out:
            check_out = datetime.strptime(check_in, "%d.%m.%Y").date()
            queryset = queryset.filter( 
                Q(check_in_date__lte=check_out) |
                Q(check_in_date__isnull=True)
            )


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
            raise Http404("Room does not exist")


def components(request):
    return render(request, 'general/components.html')
