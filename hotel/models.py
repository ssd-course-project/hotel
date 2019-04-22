from datetime import datetime

from django.db import models

from clients.models import Client


class Room(models.Model):
    AVAILABLE_STATUS = 'available'
    BOOKED_STATUS = 'booked'
    TEMPORARILY_UNAVAILABLE_STATUS = 'unavailable'

    _ROOM_STATUSES = (
        (AVAILABLE_STATUS, 'Доступный для проживания'),
        (BOOKED_STATUS, 'Забронирован'),
        (TEMPORARILY_UNAVAILABLE_STATUS, 'Временно не доступен'),
    )
    title = models.CharField(
        verbose_name="Название номера",
        blank=True,
        max_length=255
    )
    price = models.IntegerField(
        verbose_name="Цена за ночь в рублях",
        null=False, blank=False,
        default=1000
    )
    description = models.TextField(
        verbose_name="Описание номера",
        blank=True
    )
    room_size = models.IntegerField(
        verbose_name="Размер комнаты в м2",
        null=False, blank=False,
        default=20
    )
    sleeps_number = models.IntegerField(
        verbose_name="Количество человек в одном номере",
        null=False, blank=False,
        default=2
    )
    rooms_number = models.IntegerField(
        verbose_name="Количество однотипных номеров",
        null=False, blank=False,
        default=1
    )
    main_picture = models.ImageField(
        upload_to='rooms/%Y/%m/%d', blank=True, null=True
    )
    extra_services = models.ManyToManyField(
        'ExtraService',
        related_name='rooms',
        blank=True,
        verbose_name="Дополнительные услуги"
    )

    def actual_room_booking(self):
        return self.booking.filter(check_out_date__gte=datetime.now())

    def room_status(self, desired_check_in, desired_check_out):
        bookings = self.actual_room_booking()
        reserved_rooms = 0
        for booking in bookings:
            if not any((
                booking.check_in_date >= desired_check_out,
                booking.check_out_date <= desired_check_in
            )):
                reserved_rooms += 1

        free_rooms_number = self.rooms_number - reserved_rooms
        status = self.BOOKED_STATUS \
            if free_rooms_number <= 0 else self.AVAILABLE_STATUS

        return status

    class Meta:
        verbose_name = 'Фонд номеров'
        verbose_name_plural = 'Фонд номеров'

    def __str__(self):
        return "Номер {room_size}м2 на {sleeps_number} человек".format(
            room_size=self.room_size,
            sleeps_number=self.sleeps_number
        )


class ExtraPictures(models.Model):
    picture = models.ImageField(
        upload_to='rooms/%Y/%m/%d', blank=True, null=True)
    rooms = models.ForeignKey(
        Room, on_delete=models.CASCADE,
        related_name='room_pictures', blank=True, null=True
    )


class ExtraService(models.Model):
    name = models.CharField(
        verbose_name="Название услуги",
        blank=True,
        max_length=255
    )
    description = models.TextField(
        verbose_name="Описание услуги",
        blank=True
    )

    class Meta:
        verbose_name = 'Дополнительные услуги'
        verbose_name_plural = 'Дополнительные услуги'

    def __str__(self):
        return self.name
