from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from spa.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование модели привычка"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""

        # Создание пользователя для тестирования
        self.user = User.objects.create(email='test_user@test.ru',
                                        is_staff=False,
                                        is_superuser=False,
                                        is_active=True)

        self.user.set_password('qwerty')  # Устанавливаем пароль
        self.user.save()  # Сохраняем изменения пользователя в базе данных

        # Запрос токена для авторизации
        response = self.client.post('/users/token/', data={'email': self.user.email, 'password': 'qwerty'})

        self.access_token = response.data.get('access')  # Токен для авторизации

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)  # Авторизация пользователя

        # Создаем приятную привычку
        self.pleasant_habit = Habit.objects.create(place='home',
                                                   habit_time='21:00',
                                                   action='Gaming',
                                                   is_pleasant=True,
                                                   periodicity=1,
                                                   execution_time='120',
                                                   user=self.user,
                                                   is_public=True
                                                   )

        # Создаем привычку
        self.habit = Habit.objects.create(place='sports_ground',
                                          habit_time='07:00',
                                          action='Exercise',
                                          is_pleasant=False,
                                          periodicity=1,
                                          related_habit=self.pleasant_habit,
                                          execution_time='120',
                                          user=self.user
                                          )

    def test_create_habit(self):
        """Тестирование эндпоинта создание привычки"""

        # данные для привычки
        data = {
            'place': 'home',
            'habit_time': '20:00',
            'action': 'reading',
            'is_pleasant': False,
            'periodicity': 1,
            'award': 'sweetness',
            'execution_time': '100',
            'user': self.user.pk
        }

        response = self.client.post(reverse('spa:create_habit'), data=data)  # отправка запроса

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # проверяем статус ответа

        self.assertEqual(Habit.objects.all().count(), 3)  # проверяем наличия в базе данных новой записи

    def test_update_habit(self):
        """тестирование эндпоинта изменения привычки"""
        data = {'place': 'updated_sports_ground',
                'habit_time': '07:00',
                'action': 'Updated_Exercise',
                'is_pleasant': False,
                'periodicity': 1,
                'related_habit': self.pleasant_habit.pk,
                'execution_time': '120',
                'user': self.user.pk
                }

        response = self.client.patch(reverse('spa:update_habit', args=[self.habit.pk]), data=data)
        self.habit.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка статуса ответа
        self.assertEqual(self.habit.place, 'updated_sports_ground')

    def test_list_habits(self):
        """Тестирование эндпоинта отображения списка привычек"""
        response = self.client.get(reverse('spa:habit_list'))  # Запрос на получение списка привычек

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка ответа на запрос

    def test_list_public_habits(self):
        """Тестирование эндпоинта отображения списка публичных привычек"""

        response = self.client.get(reverse('spa:public_habit_list'))  # Запрос на получение списка привычек

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка ответа на запрос

    def test_execution_time_validator(self):
        """тест валидатора длительности выполнения привычки"""

        data = {'place': 'street',
                'habit_time': '09:00',
                'action': 'running',
                'is_pleasant': False,
                'periodicity': 1,
                'related_habit': self.pleasant_habit.pk,
                'execution_time': '150',
                'user': self.user.pk
                }

        response = self.client.post(reverse('spa:create_habit'), data=data)  # отправка запроса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Время выполнения привычки не должно превышать 120 секунд']})

    def test_is_pleasant_validator(self):
        """тест валидатора наличия у приятной привычки атрубута вознаграждение или связанна привычка"""

        data = {'place': 'home',
                'habit_time': '21:00',
                'action': 'Gaming',
                'is_pleasant': 'True',
                'periodicity': 1,
                'execution_time': '120',
                'user': self.user.pk,
                'is_public': True,
                'award': '200 rubles'}

        response = self.client.post(reverse('spa:create_habit'), data=data)  # отправка запроса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа
        self.assertEqual(response.json(),
                         {'non_field_errors': ['У приятной привычки не может быть '
                                               'вознаграждения или связанной привычки']}
                         )

    def test_periodicity_validator(self):
        """тест валидатора для периодичности выполнения привычки"""

        data = {'place': 'street',
                'habit_time': '09:00',
                'action': 'running',
                'is_pleasant': False,
                'periodicity': 8,
                'related_habit': self.pleasant_habit.pk,
                'execution_time': '120',
                'user': self.user.pk
                }

        response = self.client.post(reverse('spa:create_habit'), data=data)  # отправка запроса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа
        self.assertEqual(response.json(),
                         {'non_field_errors': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней']})

    def test_related_habit_validator_1(self):
        """тест валидатора создания привычки с указанием одновременно связанной привычки и вознаграждения"""

        data = {'place': 'street',
                'habit_time': '09:00',
                'action': 'running',
                'is_pleasant': False,
                'periodicity': 7,
                'related_habit': self.pleasant_habit.pk,
                'execution_time': '120',
                'user': self.user.pk,
                'award': '500 rubles'
                }

        response = self.client.post(reverse('spa:create_habit'), data=data)  # отправка запроса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа
        self.assertEqual(response.json(), {'non_field_errors': ['Невозможно одновременно указать связанную '
                                                                'привычку и вознаграждение']})

    def test_related_habit_validator_2(self):
        """тест валидатора наличия у связанной привычки признака is_pleasant"""

        data = {'place': 'street',
                'habit_time': '09:00',
                'action': 'running',
                'is_pleasant': False,
                'periodicity': 7,
                'related_habit': self.habit.pk,
                'execution_time': '120',
                'user': self.user.pk,
                }

        response = self.client.post(reverse('spa:create_habit'), data=data)  # отправка запроса
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # Проверка статуса ответа
        self.assertEqual(response.json(), {'non_field_errors': ['В связанные привычки может попасть привычка '
                                                                'с признаком приятной (is_pleasant=True)']})

    def test_destroy_habit(self):
        response = self.client.delete(reverse('spa:delete', args=[self.habit.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # Проверка статуса ответа

        self.assertEqual(Habit.objects.all().count(), 1)  # Проверка количества записей уроков в БД

    def test_create_user(self):
        """тест эндпоинта создания пользователя"""

        data = {'email': 'admin@admin.ru',
                'first_name': 'admin',
                'last_name': 'adminov',
                'is_staff': True,
                'is_superuser': True,
                'password': '12356'}

        response = self.client.post(reverse('users:user_create'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # проверяем статус ответа

        self.assertEqual(User.objects.all().count(), 2)  # проверяем наличия в базе данных новой записи