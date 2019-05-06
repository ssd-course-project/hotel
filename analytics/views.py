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

    def user_is_permitted_to_leave_feedback(self):
        try:
            client = Client.objects.get(user=self.request.user)
        except Client.DoesNotExist:
            return False
        return client.booking.all().exists()

    def get(self, request, *args, **kwargs):
        if not self.user_is_permitted_to_leave_feedback():
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
        feedback.save()
        return super().form_valid(form)


class FeedbackList(generic.TemplateView):
    template_name = "feedbacks/feedback_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user and not any((user.is_superuser, user.is_staff, user.is_anonymous)):
            try:
                client = Client.objects.get(user=user)
                context['client_has_made_booking'] = client.booking.all().exists()
            except Client.DoesNotExists:
                context['client_has_made_booking'] = False

        context['feedbacks'] = Feedback.objects.all()
        return context

