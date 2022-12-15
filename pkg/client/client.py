import random
import json

import requests


REQUEST_EXCEPTIONS = (
    requests.exceptions.JSONDecodeError,
    requests.exceptions.ProxyError,
    requests.exceptions.ConnectionError,
    json.decoder.JSONDecodeError,
    requests.exceptions.ReadTimeout
)


def sync_get(
        url: str, 
        proxy_list: list = None, 
        headers: any = None, 
        cookies: any = None
) -> requests.Response:
    """ Синхронный GET запрос
    """
    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    if proxy_list:
        proxy = random.choice(proxy_list)
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(
            url=url,
            headers=headers,
            cookies=cookies,
            proxies=proxies,
        )
    else:
        response = requests.get(
            url=url,
            headers=headers,
            cookies=cookies,
        )

    return response


def sync_post(
        url: str, 
        proxy_list: list = None, 
        headers: any = None, 
        cookies: any = None, 
        json: any = None,
        data: any = None
) -> requests.Response:
    """ Синхронный POST запрос
    """
    if headers is None:
        headers = {}
    if cookies is None:
        cookies = {}

    if proxy_list:
        proxy = random.choice(proxy_list)
        proxies = {"http": proxy, "https": proxy}
        response = requests.post(
            url=url,
            headers=headers,
            cookies=cookies,
            proxies=proxies,
            data=data,
            json=json
        )
    else:
        response = requests.post(
            url=url,
            headers=headers,
            cookies=cookies,
            data=data,
            json=json
        )

    return response
