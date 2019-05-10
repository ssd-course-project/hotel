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
    path(
        'accounts/cancel_booking/<int:booking_id>',
        login_required(views.CancelBooking.as_view()),
        name='cancel_booking'
    )
]
