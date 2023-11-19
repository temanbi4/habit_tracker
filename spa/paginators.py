from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """Класс-пагинатор для вывода списка привычек"""
    page_size = 5  # количество привычек для вывода