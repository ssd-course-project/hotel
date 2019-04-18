from django.urls import path

from . import views

urlpatterns = [
    path('feedback/new/', views.FeedbackNew.as_view(), name='feedback_new'),
    path('feedback/', views.FeedbackList.as_view(), name='feedback_list'),
]
