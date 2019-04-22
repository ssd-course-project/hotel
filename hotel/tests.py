import datetime

from django.test import TestCase
from freezegun import freeze_time

from hotel.forms import RoomBookingForm


class RoomBookingFormTest(TestCase):

    def test_form_is_valid(self):
        check_in_date = datetime.date(2019, 4, 23)
        check_out_date = datetime.date(2019, 4, 25)

        form = RoomBookingForm(
            data={
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            }
        )
        with freeze_time("2019-04-21"):
            self.assertTrue(form.is_valid())

    def test_check_in_date_before_current(self):
        error_message = "Выберите дату бронирования позднее чем сегодня"
        check_in_date = datetime.date(2019, 4, 19)
        check_out_date = datetime.date(2019, 4, 25)

        form = RoomBookingForm(
            data={
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            }
        )
        with freeze_time("2019-04-21"):
            self.assertFalse(form.is_valid())
            assert error_message == form.errors['__all__'][0]

    def test_check_out_date_before_current(self):
        error_message = "Выберите дату бронирования позднее чем сегодня"
        check_in_date = datetime.date(2019, 4, 22)
        check_out_date = datetime.date(2019, 4, 20)

        form = RoomBookingForm(
            data={
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            }
        )
        with freeze_time("2019-04-21"):
            self.assertFalse(form.is_valid())
            assert error_message == form.errors['__all__'][0]

    def test_check_in_date_after_check_out_date(self):
        error_message = "Дата отъезда не может быть раньше даты заезда"
        check_in_date = datetime.date(2019, 4, 25)
        check_out_date = datetime.date(2019, 4, 22)

        form = RoomBookingForm(
            data={
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            }
        )
        with freeze_time("2019-04-21"):
            self.assertFalse(form.is_valid())
            assert error_message == form.errors['__all__'][0]
