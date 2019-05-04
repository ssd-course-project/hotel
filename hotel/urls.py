from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoomListView.as_view(), name='room_list'),
    path('rooms/',
         login_required(views.RoomSearchView.as_view()),
         name='room_search'),
    path('room/<int:pk>/',
         login_required(views.RoomDetailView.as_view()),
         name='room_detail'),
    path('room/<int:pk>/booking',
         login_required(views.RoomBookingView.as_view()),
         name='room_booking'
    ),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
]
