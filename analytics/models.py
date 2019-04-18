from django.db import models

from clients.models import Client


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
