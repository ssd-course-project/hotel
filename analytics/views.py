from django.views import generic

from analytics.models import Feedback
from clients.models import Client
from hotel import forms


class FeedbackNew(generic.CreateView):
    model = Feedback
    template_name = 'feedbacks/feedback_new.html'
    fields = ('rating', 'text')
    success_url = '/'

    def form_valid(self, form):
        feedback = form.save(commit=False)
        user = self.request.user
        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            raise forms.ValidationError("You are not our client!")
        feedback.author = client
        feedback.save()
        return super().form_valid(form)


class FeedbackList(generic.ListView):
    model = Feedback
    template_name = "feedbacks/feedback_list.html"
    context_object_name = 'feedbacks'