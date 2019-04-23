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


class RoomSearchViewTest(TestCase):

    def test_general_get_request(self):
        response = self.client.get("/rooms/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/room_search.html")

    def test_get_request_without_date(self):
        response = self.client.get("/rooms/", {"check_in_date": "2019-04-21"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/room_search.html")
        self.assertFalse(False, "Введите дату заезда и выезда")

    def test_get_request_with_dates(self):
        response = self.client.get("/rooms/", {"check_in_date": "2019-04-21", "check_out_date": "2019-04-25"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/room_search.html")
        self.assertTrue(True, response.content)

    def test_get_request_with_visitors(self):
        response = self.client.get('/rooms/', {"visitors": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/room_search.html')
        self.assertTrue(True, response.content)

    def test_get_request_with_price(self):
        response = self.client.get('/rooms/', {"price": "10000"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hotel/room_search.html')
        self.assertTrue(True, response.content)
