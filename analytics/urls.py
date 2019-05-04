from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('feedback/new/',
         login_required(views.FeedbackNew.as_view()),
         name='feedback_new'),
    path('feedback/', views.FeedbackList.as_view(), name='feedback_list'),
]
