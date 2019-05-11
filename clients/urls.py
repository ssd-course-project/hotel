from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path(
        'accounts/profile/',
        login_required(views.ProfileView.as_view()),
        name='base_profile'
    ),
]
