from datetime import datetime, timezone

from celery import shared_task

from spa.models import Habit
from spa.utils import send_telegram_message


@shared_task
def check_habits():
    """Задача для периодического запуска.
    Поиск привычек, проверка на соответствие текущего времени и времени,
    заложенного в атрибут habit_time модели Привычка и отправки сообщения в телеграмм"""

    current_datetime = datetime.now().replace(second=0, microsecond=0)  # текущая дата/время
    current_time = current_datetime.time().replace(second=0, microsecond=0)  # текущее время без секунд и микросекунд

    habits = Habit.objects.all()  # все привычки

    for habit in habits:

        # время выполнения привычки без секунд и микросекунд
        habit_time = habit.habit_time.replace(second=0, microsecond=0)

        # если время привычки равно текущему времени без учета секунд
        if habit_time == current_time:

            # Если привычка никогда не выполнялась
            if not habit.last_execution_time:
                send_telegram_message(habit)  # вызов функции отправки сообщения
                habit.last_execution_time = datetime.now(timezone.utc)
                habit.save()
            else:
                # вычисляем количество дней с момента последнего выполнения привычки
                days_from_last_execution = datetime.now(timezone.utc) - habit.last_execution_time

                # если оно совпадает с периодичностью привычки отправляем напоминание
                if days_from_last_execution.days == habit.periodicity:
                    send_telegram_message(habit)  # вызов функции отправки сообщения