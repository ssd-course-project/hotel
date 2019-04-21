from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError


class RoomBookingForm(forms.Form):
    check_in_date = forms.DateField(
        label="Начало бронирования:",
        help_text="Выберите дату заезда",
        widget=forms.SelectDateWidget(
            empty_label=("Год", "Месяц", "День"),
        )
    )
    check_out_date = forms.DateField(
        label="Конец бронирования:",
        help_text="Выберите дату отъезда",
        widget=forms.SelectDateWidget(
            empty_label=("Год", "Месяц", "День"),
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        current_date = datetime.now().date()
        if any((
            check_in_date < current_date,
            check_out_date <= current_date
        )):
            raise ValidationError(
                "Выберите дату бронирования позднее чем сегодня"
            )

        if check_in_date >= check_out_date:
            raise ValidationError(
                "Дата отъезда не может быть раньше даты заезда"
            )
