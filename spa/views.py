from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from spa.models import Habit
from spa.paginators import HabitPaginator
from spa.serializers import HabitSerializer


class HabitListAPIView(generics.ListAPIView):
    """Класс-представление для отображения списка привычек текущего пользователя"""

    serializer_class = HabitSerializer  # Сериализатор
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
    pagination_class = HabitPaginator  # пагинатор

    def get_queryset(self):
        """Фильтрация привычек текущего пользователя"""

        queryset = Habit.objects.filter(user=self.request.user).order_by('user')

        return queryset


class PublicHabitListAPIView(generics.ListAPIView):
    """Класс-представление для отображения списка всех публичных привычек на основе generics"""

    serializer_class = HabitSerializer  # Сериализатор
    queryset = Habit.objects.filter(is_public=True)  # фильтр
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей
    pagination_class = HabitPaginator  # пагинатор


class HabitCreateAPIView(generics.CreateAPIView):
    """Класс-представление для создания привычки на основе generics"""
    serializer_class = HabitSerializer  # Сериализатор
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей

    def perform_create(self, serializer):
        """Добавление пользователя создаваемой привычке"""

        new_habit = serializer.save()  # сохранение привычки
        new_habit.user = self.request.user  # добавляем пользователя
        new_habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Класс-представление для обновления привычки на основе generics"""
    serializer_class = HabitSerializer  # Сериализатор
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей

    def get_queryset(self):
        """Фильтрация привычек текущего пользователя"""
        queryset = Habit.objects.filter(user=self.request.user)
        return queryset


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Класс-представление для удаления привычки на основе generics"""
    queryset = Habit.objects.all()  # Фильтр
    permission_classes = [IsAuthenticated]  # Только для авторизованных пользователей

    def get_queryset(self):
        """Фильтрация привычек текущего пользователя"""

        queryset = Habit.objects.filter(user=self.request.user)
        return queryset
