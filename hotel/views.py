from django.shortcuts import render
from django.views import generic
from .models import Room


class RoomList(generic.ListView):
    model = Room
    template_name = "room_list.html"
    context_object_name = 'rooms'


class RoomDetail(generic.DetailView):
    model = Room
    context_object_name = 'room'
    context_object_name2 = 'extra_services'


def index(request):
    return render(request, 'index.pug')
