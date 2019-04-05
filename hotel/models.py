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
    extra_services = models.ManyToManyField(
        'ExtraService',
        related_name='rooms',
        verbose_name="Дополнительные услуги")

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
    name = models.TextField(
        verbose_name="Название услуги",
        blank=True
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


class Feedback(models.Model):
    author = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
    )
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default='5',
        verbose_name='Оценка'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )

    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.name

