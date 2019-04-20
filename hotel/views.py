from django import forms
from django.db.models import Q
from django.forms.models import modelform_factory
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


class RoomBookingView(generic.UpdateView):
    model = Room
    form_class = modelform_factory(
        Room,
        form=RoomBookingForm
    )
    template_name = 'hotel/room_booking.html'
    context_object_name = 'room'
    success_url = '/'

    def form_valid(self, form):
        room = form.save(commit=False)
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            raise forms.ValidationError("You are not our client!")
        room.renter = client
        room.room_status = room.BOOKED_STATUS

        RoomBooking.objects.create(
            room=room,
            renter=client,
            check_in_date=room.check_in_date,
            check_out_date=room.check_out_date
        )

        room.save(update_fields=["renter", "room_status"])
        return super().form_valid(form)


def components(request):
    return render(request, 'general/components.html')
