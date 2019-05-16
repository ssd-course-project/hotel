from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render
from django.views import generic, View
from django.shortcuts import redirect

from analytics.models import RoomBooking
from clients.models import Client
from hotel.forms import RoomBookingForm, RoomSearchForm
from .models import Room


class RoomListView(generic.ListView):
    model = Room
    template_name = "hotel/room_list.html"
    context_object_name = 'rooms'


class RoomSearchView(generic.edit.FormMixin, generic.ListView):
    model = Room
    template_name = "hotel/room_search.html"
    form_class = RoomSearchForm
    context_object_name = 'rooms'
    ERROR_MESSAGE = "Недостаточно данных для поиска или они некорректные"

    def get(self, request, *args, **kwargs):
        if self.request.GET:
            form = self.form_class(self.request.GET)

            if not form.is_valid():
                return render(
                    request,
                    self.template_name,
                    {'form': form, 'error_message': self.ERROR_MESSAGE}
                )

            self.object_list = self.get_queryset()
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
        else:
            return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.GET:
            return queryset

        check_in = self.request.GET.get('check_in_date')
        check_out = self.request.GET.get('check_out_date')
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
    success_url = '/success'
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
            return redirect('error')

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


class CancelBookingView(View):
    def post(self, request, booking_id, *args, **kwargs):

        try:
            booking = RoomBooking.objects.get(id=booking_id)
        except RoomBooking.DoesNotExist:
            raise Http404

        try:
            client = Client.objects.get(user=request.user)
        except Client.DoesNotExist:
            client = None

        if booking.renter == client:
            booking.is_cancelled = True
            booking.save()
            return redirect('base_profile')
        else:
            raise PermissionDenied()
