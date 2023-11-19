from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class Habit(models.Model):
    """Модель привычки"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE,
                             **NULLABLE)  # пользователь (добавляется автоматически из авторизованного)
    place = models.CharField(max_length=255, verbose_name='Место')  # место выполнения привычки
    habit_time = models.TimeField(verbose_name='Время выполнения')  # Время, когда необходимо выполнить привычку
    action = models.CharField(max_length=255, verbose_name='Действие')  # действие для привычки
    is_pleasant = models.BooleanField(verbose_name='Приятная привычка')  # Признак приятной привычки
    related_habit = models.ForeignKey('self', verbose_name='Связанная привычка',
                                      on_delete=models.SET_NULL,
                                      **NULLABLE)  # связанная привычка (для полезной)
    periodicity = models.IntegerField(verbose_name='Периодичность')  # периодичность выполнения привычки в днях.
    award = models.CharField(max_length=255,
                             verbose_name='Вознаграждение',
                             **NULLABLE)  # вознаграждение за выполнение привычки
    execution_time = models.DurationField(verbose_name='Время выполнения')  # время, потраченное на выполнение привычки
    is_public = models.BooleanField(default=False, verbose_name='Публичность')  # признак публичности
    last_execution_time = models.DateTimeField(**NULLABLE, verbose_name='Время последнего выполнения привычки')