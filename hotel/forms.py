from django import forms
from django.core.exceptions import ValidationError

from .models import Room, Feedback


class RoomBookingForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if not any((check_in_date, check_out_date)):
            raise ValidationError(
                "Вы должны заполнить даты заезда!"
            )

        if check_in_date >= check_out_date:
            raise ValidationError(
                "Дата отъезда не может быть раньше даты заезда"
            )

    class Meta:
        model = Room
        fields = ['check_in_date', 'check_out_date']
        labels = {
            'check_in_date': ("Начало бронирования:"),
            'check_out_date': ('Конец бронирования:'),
        }
        help_texts = {
            'check_in_date': ('Выберите дату заезда'),
            'check_out_date': ('Выберите дату отъезда'),
        }
        widgets = {
            'check_in_date': forms.SelectDateWidget(
                empty_label=("Год", "Месяц", "День"),
            ),
            'check_out_date': forms.SelectDateWidget(
                empty_label=("Год", "Месяц", "День"),
            ),
        }


class FeedbackForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text')

        if not rating:
            raise ValidationError(
                "Вы должны выбрать оценку!"
            )

        if not text:
            raise ValidationError(
                "Вы должны заполнить поле отзыва!"
            )

    class Meta:
        model = Feedback
        fields = ['rating', 'text']
