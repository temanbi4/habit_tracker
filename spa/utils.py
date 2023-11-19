import requests
from config import settings


def send_telegram_message(habit, chat_id='453548340'):
    """Функция для отправки сообщения в Telegram."""
    try:
        token = settings.TELEGRAM_TOKEN
        award = habit.award if habit.award else (habit.related_habit.action if habit.related_habit else None)

        text = (
            f'Привет. Это напоминание о привычке:'
            f' место - {habit.place}, действие - {habit.action}, время выполнения - {habit.execution_time},'
            f' вознаграждение - {award}'
        )

        data = {'chat_id': chat_id, 'text': text}
        response = requests.post(f'https://api.telegram.org/bot{token}/sendMessage?', data=data)

        response.raise_for_status()  # Проверка на ошибки при отправке запроса
    except requests.RequestException as e:
        print(f"Ошибка при отправке сообщения в Telegram: {e}")
