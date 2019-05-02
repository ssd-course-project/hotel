from django.core.exceptions import ValidationError
from django.views import generic

from clients.forms import RegistrationForm
from clients.models import Client


class RegisterView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/accounts/login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProfileView(generic.TemplateView):
    template_name = 'clients/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user and not any((user.is_superuser, user.is_staff)):
            try:
                context['client'] = Client.objects.get(user=user)
            except Client.DoesNotExist:
                raise ValidationError("You are not our client!")

        if user:
            try:
                client = Client.objects.get(user=user)
            except Client.DoesNotExist:
                if any((user.is_superuser, user.is_staff)):
                    client = Client.objects.create(
                        user=user,
                        name="Admin {}".format(user.username),
                        phone=+71111111111,
                        email=user.email
                    )
                else:
                    raise ValidationError("You are not our client!")
            context['client'] = client

        return context
