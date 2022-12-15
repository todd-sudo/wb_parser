import requests
from django.conf import settings


def send_message_to_telegram(message: str):
    """ Отправляет сообщение в телеграм
    """
    url = f'https://api.telegram.org/bot{settings.TELEGRAM_API_KEY}/sendMessage'
    data = {'chat_id': settings.TELEGRAM_CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    return response
