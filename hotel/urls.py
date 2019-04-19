from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoomListView.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path(
        'room/<int:pk>/booking',
        login_required(views.RoomBookingView.as_view()),
        name='room_booking'
    ),
]
