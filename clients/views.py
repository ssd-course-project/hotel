from django.views import generic
from django.db.models import Q

from clients.forms import RegistrationForm
from clients.models import Client
from django.shortcuts import redirect

from datetime import date


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

        try:
            client = Client.objects.get(user=user)
        except Client.DoesNotExist:
            if any((user.is_superuser, user.is_staff)):
                client = Client.objects.create(
                    user=user,
                    name="Admin {}".format(user.username),
                    phone="+71111111111",
                    email=user.email
                )
            else:
                return None

        now = date.today()
        current_bookings = client.booking.filter(Q(is_cancelled=False) &
                                                 Q(check_out_date__gte=now)).order_by('-created_at')
        bookings_archive = client.booking.filter(Q(is_cancelled=True) |
                                                 Q(check_out_date__lt=now)).order_by('-created_at')

        context['client'] = client
        context['current_bookings'] = current_bookings
        context['bookings_archive'] = bookings_archive

        return context

    def render_to_response(self, context, **response_kwargs):
        if context is None:
            return redirect('error')
        return super().render_to_response(context, **response_kwargs)
