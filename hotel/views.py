from idlelib.idle_test.test_help_about import About

from django import forms
from django.forms.models import modelform_factory
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


def about(request):
    return render(request, 'hotel/about_list.html')


def contacts(request):
    return render(request, 'hotel/contacts_list.html')


