from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователь"""

    class Meta:
        model = User  # Модель
        fields = '__all__'  # ПОля

    def save(self, **kwargs):
        """Сохранение пользователя в базу данных"""

        data = super().save(**kwargs)
        data.set_password(self.validated_data['password'])  # Задание пароля
        data.save()  # Сохранение в базе данных

        return data
