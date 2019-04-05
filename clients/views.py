from django.views import generic

from .forms import RegistrationForm


class RegisterView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
