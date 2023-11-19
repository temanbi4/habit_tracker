from django.urls import path

from spa.apps import SpaConfig
from spa.views import (HabitListAPIView, PublicHabitListAPIView, HabitCreateAPIView, HabitUpdateAPIView,
                       HabitDestroyAPIView)

app_name = SpaConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habit_list'),
    path('habits/public/', PublicHabitListAPIView.as_view(), name='public_habit_list'),
    path('habits/create/', HabitCreateAPIView.as_view(), name='create_habit'),
    path('habits/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='update_habit'),
    path('habits/delete/<int:pk>/', HabitDestroyAPIView.as_view(), name='delete'),
]