from django.shortcuts import render
from django.views import generic
from django import forms
from clients.models import Client
from .models import Room, Feedback


class RoomList(generic.ListView):
    model = Room
    template_name = "hotel/room_list.html"
    context_object_name = 'rooms'


class RoomDetail(generic.DetailView):
    model = Room
    context_object_name = 'room'


class FeedbackNew(generic.CreateView):
    model = Feedback
    template_name = 'hotel/feedback_new.html'
    fields = ('rating', 'text')
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


def index(request):
    return render(request, 'index.pug')

