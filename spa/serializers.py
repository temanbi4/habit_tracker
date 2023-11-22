from rest_framework import serializers

from spa.models import Habit
from spa.validators import ExecutionTimeValidator, PeriodicityValidator, RelatedHabitValidation, IsPleasantValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор модели Привычка (Habit)"""

    class Meta:
        model = Habit
        fields = '__all__'

        # Валидаторы
        validators = [ExecutionTimeValidator(field='execution_time'),
                      PeriodicityValidator(field='periodicity'),
                      RelatedHabitValidation(field='related_habit'),
                      IsPleasantValidator(field='is_pleasant')]
