from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Client


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    name = forms.CharField(label="ФИО")
    phone = forms.CharField(label="Контактный телефон")

    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone')

    def save(self, **kwargs):
        user = super().save()

        Client.objects.create(
            user=user,
            name=self.cleaned_data["name"],
            phone=self.cleaned_data["phone"],
            email=self.cleaned_data["email"]
        )
        return user

