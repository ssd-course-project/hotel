from django.shortcuts import render
from django.views import generic
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
    fields = ('name', 'rating', 'text')
    template_name_suffix = '_new'
    success_url = '/feedback/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class FeedbackList(generic.ListView):
    model = Feedback
    template_name = "hotel/feedback_list.html"
    context_object_name = 'feedbacks'


def index(request):
    return render(request, 'index.pug')

