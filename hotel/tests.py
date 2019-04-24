import datetime

from django.test import TestCase, Client
from django.urls import reverse
from freezegun import freeze_time

from hotel.forms import RoomBookingForm
from hotel.models import Room


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

    def setUp(self):
        self.client = Client()
        self.url = reverse('room_search')
        self.room1 = Room.objects.create(
            title='testRoom1',
            price=20000,
            sleeps_number=2,
            main_picture='../hotel/static/vendors/images/general/background.png'
        )
        self.room2 = Room.objects.create(
            title='testRoom2',
            price=10000,
            sleeps_number=3,
            main_picture='../hotel/static/vendors/images/general/background.png'
        )
        self.booking1 = RoomBookingForm(
            data={
                "room": self.room1,
                "check_in_date": datetime.date(2019, 4, 21),
                "check_out_date": datetime.date(2019, 4, 25)
            }
        )
        self.booking1 = RoomBookingForm(
            data={
                "room": self.room2,
                "check_in_date": datetime.date(2019, 5, 21),
                "check_out_date": datetime.date(2019, 5, 25)
            }
        )

    def test_general_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/room_search.html")
        self.assertQuerysetEqual(
            response.context['rooms'],
            ['<Room: Номер 20м2 на 2 человек>', '<Room: Номер 20м2 на 3 человек>'],
            ordered=False
        )

    def test_get_request_without_date(self):
        error_message = "" \
                        "Введите дату заезда и выезда, чтобы мы могли показать вам " \
                        "доступные в это время номера"
        response = self.client.get(
            self.url,
            {"check_in_date": "2019-04-21"}
        )
        self.assertEqual(error_message, response.context_data.get('error_message'))
        # self.assertQuerysetEqual(response.context['rooms'], [])

    def test_get_request_with_dates(self):
        response = self.client.get(
            self.url, {
                "check_in_date": "2019-04-21",
                "check_out_date": "2019-04-25"
            }
        )
        self.assertEqual(response.status_code, 200)
        # self.assertQuerysetEqual(
        #     response.context['rooms'],
        #     ['<Room: Номер 20м2 на 2 человек>']
        # )

    def test_get_request_with_visitors(self):
        response = self.client.get(
            self.url,
            {"visitors": "2"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['rooms'],
            ['<Room: Номер 20м2 на 2 человек>']
        )

    def test_get_request_with_price(self):
        response = self.client.get(
            self.url,
            {"price": "10000"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['rooms'],
            ['<Room: Номер 20м2 на 3 человек>']
        )
