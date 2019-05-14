import datetime

from django import forms
from django.core.exceptions import ValidationError


class RoomBookingForm(forms.Form):
    check_in_date = forms.DateField(
        label="Начало бронирования:",
        help_text="Выберите дату заезда"
    )
    check_out_date = forms.DateField(
        label="Конец бронирования:",
        help_text="Выберите дату отъезда",
    )

    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if not all((
            check_in_date,
            check_out_date,
            isinstance(check_in_date, datetime.date),
            isinstance(check_out_date, datetime.date)
        )):
            raise ValidationError(
                "Введены некорретные даты"
            )

        current_date = datetime.datetime.now().date()
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


class RoomSearchForm(RoomBookingForm):
    NUMBER_OF_VISITORS = (
        ("", ""),
        ("1", '1 Гость'),
        ("2", '2 Гостя'),
        ("3", '3 Гостя'),
        ("4", '4 Гостя'),
    )
    price = forms.IntegerField(
        label="Максимальная цена за ночь, рублей",
        help_text="Укажите цену",
        required=False
    )
    visitors = forms.CharField(
        label="Количество гостей",
        widget=forms.Select(choices=NUMBER_OF_VISITORS),
        required=False
    )

    def clean(self):
        super().clean()
        visitors = self.cleaned_data.get('visitors')

        if not any((
            visitors == pair[0] for pair in self.NUMBER_OF_VISITORS
        )):
            raise ValidationError(
                "Введено некорректное значение гостей"
            )
