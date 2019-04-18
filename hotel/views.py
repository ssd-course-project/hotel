from django import forms
from django.forms.models import modelform_factory
from django.shortcuts import render
from django.views import generic

from clients.models import Client
from hotel.forms import RoomBookingForm, FeedbackForm
from .models import Room, Feedback


class RoomList(generic.ListView):
    model = Room
    template_name = "hotel/room_list.html"
    context_object_name = 'rooms'


class RoomDetail(generic.DetailView):
    model = Room
    context_object_name = 'room'


class RoomBooking(generic.UpdateView):
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
        room.save(update_fields=["renter", "room_status"])
        return super().form_valid(form)


class FeedbackNew(generic.FormView):
    form_class = FeedbackForm
    template_name = 'hotel/feedback_new.html'
    success_url = '/'

    def form_valid(self, form):
        feedback = form.save(commit=False)
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            raise forms.ValidationError("You are not our client!")
        feedback.author = client
        feedback.save()
        return super().form_valid(form)


class FeedbackList(generic.ListView):
    model = Feedback
    template_name = "hotel/feedback_list.html"
    context_object_name = 'feedbacks'


def components(request):
    return render(request, 'general/components.html')
