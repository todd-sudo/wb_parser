from typing import Optional

from app.models import Proxy


def get_proxy_list() -> Optional[list]:
    proxies = list(Proxy.objects.all())
    if not proxies:
        return None
    proxy_list = []
    for p in proxies:
        proxy_list.append(
            f"http://{p.username}:{p.password}@{p.host}:{p.port}")
    return proxy_list
