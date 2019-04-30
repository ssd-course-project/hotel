import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time

from analytics.models import RoomBooking
from hotel.forms import RoomBookingForm
from hotel.models import Room
from clients.models import Client


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
        self.url = reverse('room_search')
        self.user = User.objects.create(
            username='testuser',
            email='test@test.com',
            password='qwerty123',
        )
        self.renter = Client.objects.create(
            user=self.user,
            name='test',
            phone=88005553535,
            email='test@test.com'
        )
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
        self.booking = RoomBooking.objects.create(
            room=self.room1,
            renter=self.renter,
            check_in_date=datetime.date(2019, 4, 21),
            check_out_date=datetime.date(2019, 4, 25)
        )

    def test_general_get_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/room_search.html")
        self.assertQuerysetEqual(
            response.context.get('object_list'),
            map(repr, [self.room1, self.room2]),
            ordered=False
        )

    def test_get_request_without_date(self):
        error_message = "" \
                        "Введите дату заезда и выезда, чтобы мы могли " \
                        "показать Вам доступные в это время номера"
        with freeze_time("2019-04-21"):
            response = self.client.get(
                self.url,
                {"check_in": "22.04.2019"}
            )
        self.assertEqual(
            error_message,
            response.context_data.get('error_message')
        )
        self.assertQuerysetEqual(
            response.context.get('object_list'),
            map(repr, [self.room1, self.room2]),
            ordered=False
        )

    def test_get_request_with_dates(self):
        with freeze_time("2019-04-21"):
            response = self.client.get(
                self.url, {
                    "check_in": "22.04.2019",
                    "check_out": "24.04.2019"
                }
            )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context.get('object_list'),
            map(repr, [self.room2])
        )

    def test_get_request_with_visitors(self):
        response = self.client.get(
            self.url,
            {"visitors": "2"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context.get('object_list'),
            map(repr, [self.room1])
        )

    def test_get_request_with_price(self):
        response = self.client.get(
            self.url,
            {"price": "10000"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context.get('object_list'),
            map(repr, [self.room2])
        )


class RoomBookingViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='usertest',
            email='test1@test.com',
            password='ABC123',
        )
        self.renter = Client.objects.create(
            user=self.user,
            name='test1',
            phone=89882445511,
            email='test1@test.com'
        )
        self.room = Room.objects.create(
            title='testRoom',
            price=1000,
            sleeps_number=2,
            rooms_number=1,
            main_picture='../hotel/static/vendors/images/general/background.png'
        )
        self.booking = RoomBooking.objects.create(
            room=self.room,
            renter=self.renter,
            check_in_date=datetime.date(2019, 5, 21),
            check_out_date=datetime.date(2019, 5, 23)
        )

    def test_room_status_with_same_as_existing_booking_date(self):
        with freeze_time("2019-05-11"):
            room_status = self.room.room_status(
                datetime.date(2019, 5, 21),
                datetime.date(2019, 5, 23)
            )
        self.assertTrue(room_status == self.room.BOOKED_STATUS)

    def test_room_status_after_booking_dates(self):
        with freeze_time("2019-05-11"):
            room_status = self.room.room_status(
                datetime.date(2019, 5, 24),
                datetime.date(2019, 5, 25)
            )
        self.assertTrue(room_status == self.room.AVAILABLE_STATUS)

    def test_room_status_outside_booking_dates(self):
        with freeze_time("2019-05-11"):
            room_status = self.room.room_status(
                datetime.date(2019, 5, 20),
                datetime.date(2019, 5, 24)
            )
        self.assertTrue(room_status == self.room.BOOKED_STATUS)

    def test_room_status_between_the_first_booking_date(self):
        with freeze_time("2019-05-11"):
            room_status = self.room.room_status(
                datetime.date(2019, 5, 20),
                datetime.date(2019, 5, 22)
            )
        self.assertTrue(room_status == self.room.BOOKED_STATUS)

    def test_room_status_between_the_second_booking_date(self):
        with freeze_time("2019-05-11"):
            room_status = self.room.room_status(
                datetime.date(2019, 5, 22),
                datetime.date(2019, 5, 24)
            )
        self.assertTrue(room_status == self.room.BOOKED_STATUS)

    def test_room_status_before_booking_dates(self):
        with freeze_time("2019-05-11"):
            room_status = self.room.room_status(
                datetime.date(2019, 5, 19),
                datetime.date(2019, 5, 20)
            )
        self.assertTrue(room_status == self.room.AVAILABLE_STATUS)
