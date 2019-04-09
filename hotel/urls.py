from django.urls import path

from . import views

urlpatterns = [
    path('', views.RoomList.as_view(), name='room_list'),
    path('room/<int:pk>/', views.RoomDetail.as_view(), name='room_detail'),
    path('feedback/new/', views.FeedbackNew.as_view(), name='feedback_new'),
    path('feedback/', views.FeedbackList.as_view(), name='feedback_list'),
    path('components/', views.components, name='index'),
    path('pug/', views.pug, name='pug'),
]
