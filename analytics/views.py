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

    def dispatch(self, *args, **kwargs):
        client = Client.objects.get(user=self.request.user)
        if not client.booking.all().exists():
            return redirect('feedback_list')
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        feedback = form.save(commit=False)
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            return redirect('error')
        feedback.author = client
        feedback.save()
        return super().form_valid(form)


class FeedbackList(generic.TemplateView):
    template_name = "feedbacks/feedback_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user and not any((user.is_superuser, user.is_staff)):
            client = Client.objects.get(user=user)
            bookings = client.booking.all()
            context['client_has_made_booking'] = bookings.exists()

        context['feedbacks'] = Feedback.objects.all()
        return context

