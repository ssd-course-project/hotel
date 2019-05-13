from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoomListView.as_view(), name='room_list'),
    path('rooms/', views.RoomSearchView.as_view(), name='room_search'),
    path('room/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('room/<int:pk>/booking',
         login_required(views.RoomBookingView.as_view()),
         name='room_booking'
    ),
    path(
        'booking/<int:booking_id>/cancel',
        login_required(views.CancelBookingView.as_view()),
        name='cancel_booking'
    ),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('error/', views.error, name='error'),
    path('success/', views.success, name='success')
]
