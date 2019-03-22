from django.db import models


class Room(models.Model):
    AVAILABLE_STATUS = 'available'
    BOOKED_STATUS = 'booked'
    TEMPORARILY_UNAVAILABLE_STATUS = 'unavailable'

    _ROOM_STATUSES = (
        (AVAILABLE_STATUS, 'Доступный для проживания'),
        (BOOKED_STATUS, 'Забронирован'),
        (TEMPORARILY_UNAVAILABLE_STATUS, 'Временно не доступен'),
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
    room_status = models.CharField(
        verbose_name='Статус номера', max_length=255,
        choices=_ROOM_STATUSES, default=AVAILABLE_STATUS
    )
    check_in_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата начала бронирования',
        help_text='Дата с которой номер меняет статус на "забронирован"'
    )
    check_out_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата конца бронирования',
        help_text='Дата с которой номер меняет статус на "свободный"'
    )
    main_picture = models.ImageField(
        upload_to='rooms/%Y/%m/%d', blank=True, null=True
    )

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


class AdditionalService(models.Model):
    description = models.TextField(
        verbose_name="Описание услуги",
        blank=True
    )
    name = models.TextField(
        verbose_name="Название услуги",
        blank=True
    )
