from django.db import models

from clients.models import Client
from hotel.models import Room


class Feedback(models.Model):
    RATING_CHOICES = (
        (1, 'Ужасно'),
        (2, 'Плохо'),
        (3, 'Средне'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    )

    author = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания'
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
        return "Отзыв от {}".format(self.author)


class RoomBooking(models.Model):
    renter = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name='Арендатор',
        related_name='booking',
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name='Номер',
        related_name='booking'
    )
    check_in_date = models.DateField(verbose_name='Дата начала бронирования')
    check_out_date = models.DateField(verbose_name='Дата конца бронирования')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время бронирования'
    )

    class Meta:
        verbose_name = 'Бронирование номера'
        verbose_name_plural = 'Бронирования номеров'

    def __str__(self):
        return "Забронирован номер {}".format(self.room)
