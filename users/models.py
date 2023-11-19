from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')
    telegram_id = models.CharField(max_length=100, verbose_name='Телеграм ID пользователя', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []