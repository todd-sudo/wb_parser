""" Сервисы
"""
import random
import time

import requests
from fake_useragent import UserAgent


def write_state_parser(_state: str) -> None:
    """
    Перезаписывает состояние парсера, нужен для того чтобы при повторном POST
    запросе, на клиентскую сторону прилетал 405 статус код
    """
    with open('state_parsing.json', 'w') as state:
        st = '{' + f'"parser_state": {_state}' + '}'
        state.write(st)


def get_new_json(product_id) -> str:
    """Получает новые данные в формате json по артикулу товара """
    headers = {
        'User-Agent': user_agent(),
    }
    url = f'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?' \
          f'spp=12&pricemarginCoeff=1.0&reg=1&appType=1&' \
          f'offlineBonus=0&onlineBonus=0&emp=0&locale=ru&' \
          f'lang=ru&curr=rub&nm={product_id}'
    r = requests.get(url, headers)
    return r.text


def user_agent() -> any:
    """Возвращает рандомный user-agent"""
    ua = UserAgent()
    return ua.random


def delay() -> None:
    """Засыпает"""
    time.sleep(random.randint(2, 4))
