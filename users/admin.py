from django.contrib import admin
from users.models import User

# Register your models here.

admin.site.register(User)  # регистрация модели "пользователь" в админ-панели
