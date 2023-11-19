from datetime import timedelta

from rest_framework.exceptions import ValidationError

from spa.tasks import check_habits







class ExecutionTimeValidator:
    """Проверка длительности поля execution_time"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        execution_time = value[self.field]
        check_habits()

        if execution_time > timedelta(seconds=120):
            raise ValidationError('Время выполнения привычки не должно превышать 120 секунд')


class RelatedHabitValidation:
    """Проверка наличия у связанной привычки признака is_pleasant"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        award = value.get('award')
        related_habit = value.get('related_habit')

        if award is not None and related_habit is not None:
            raise ValidationError('Невозможно одновременно указать связанную привычку и вознаграждение')

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError('В связанные привычки может попасть привычка с признаком приятной (is_pleasant=True)')


class IsPleasantValidator:
    """У приятной привычки не может быть вознаграждения или связанной привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        is_pleasant = value[self.field]

        if is_pleasant and (value.get('award') or value.get('related_habit')):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')


class PeriodicityValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = value.get(self.field)

        if periodicity is not None and periodicity > 7:
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')
