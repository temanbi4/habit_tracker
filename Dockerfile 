# мспользование образа python3
FROM python:3

# заданем рабочую директорию
WORKDIR /course_work8

# копируем файл с зависимостями пректа в рабочую директорию
COPY ./requirements.txt /course_work8/

# запускаем установку зависимостей
RUN pip install -r requirements.txt

# копируем все файлы из текущей директории в рабочую директорию
COPY . .