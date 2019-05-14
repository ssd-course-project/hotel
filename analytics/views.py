from datetime import date

from django.views import generic

from analytics.models import Feedback
from clients.models import Client
from hotel import forms
from django.shortcuts import redirect


class FeedbackNew(generic.CreateView):
    model = Feedback
    template_name = 'feedbacks/feedback_new.html'
    fields = ('rating', 'text')
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if not self.is_user_permitted_to_leave_feedback():
            return redirect('feedback_list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        feedback = form.save(commit=False)
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            return redirect('error')
        feedback.author = client
        return super().form_valid(form)

    def is_user_permitted_to_leave_feedback(self):
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            client = None

        if any((not client, user.is_superuser, user.is_staff)):
            return False
        else:
            return client.booking.filter(
                is_cancelled=False, check_out_date__lt=date.today()
            ).exists()


class FeedbackList(generic.ListView):
    model = Feedback
    template_name = "feedbacks/feedback_list.html"
    context_object_name = 'feedbacks'

    def get_queryset(self):
        return Feedback.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not any((user.is_superuser, user.is_staff, user.is_anonymous)):
            try:
                client = Client.objects.get(user=user)
            except Client.DoesNotExist:
                client = None

            context['client_has_made_booking'] = client.booking.filter(
                is_cancelled=False, check_out_date__lt=date.today()
            ).exists() if client else False

        return context
