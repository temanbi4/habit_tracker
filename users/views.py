from rest_framework import generics

from users.serializers import UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Создание (регистрация) нового пользователя"""

    serializer_class = UserSerializer
