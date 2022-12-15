from typing import Optional

import requests

from pkg.client.client import sync_get, sync_post
from pkg.client.client import REQUEST_EXCEPTIONS


def request_retry(
        url: str, headers: dict, proxy_list: list = None, cookies=None
) -> Optional[requests.Response]:
    if cookies is None:
        cookies = {}
    for i in range(1, 11):
        try:
            print(f"Request retry: {i} Url: {url}")
            response = sync_get(
                url=url, headers=headers, cookies=cookies, proxy_list=proxy_list
            )
            if response and response.status_code == 200:
                return response
        except REQUEST_EXCEPTIONS as err:
            print(err)
            continue
    return None


def request_retry_post(
        url: str, 
        headers: dict, 
        proxy_list: list = None, 
        cookies: any = None, 
        json: any = None, 
        data: any = None
) -> Optional[requests.Response]:
    if cookies is None:
        cookies = {}
    for i in range(1, 11):
        try:
            print(f"Request retry: {i} Url: {url}")
            response = sync_post(
                url=url, 
                headers=headers, 
                cookies=cookies, 
                proxy_list=proxy_list, 
                data=data,
                json=json
            )
            if response and response.status_code == 200:
                return response
        except REQUEST_EXCEPTIONS as err:
            print(err)
            continue
    return None
