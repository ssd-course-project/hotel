from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoomList.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetail.as_view(), name='room_detail'),
]
