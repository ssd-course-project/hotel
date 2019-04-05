from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client',
        verbose_name='Клиент',
        null=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='ФИО',
    )
    phone = models.CharField(
        max_length=255,
        verbose_name='Телефон'
    )
    email = models.EmailField(
        max_length=255,
        verbose_name='Email для связи'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name

