import concurrent.futures
from typing import List

from django.conf import settings

from app.models import ProductWB
from app.parser.content import get_content_products
from app.parser.feedback import get_feedbacks_product
from app.parser.price import get_price_products
from pkg.helper.get_proxy import get_proxy_list
from config import celery_app
from pkg.helper.telegram import send_message_to_telegram

SIZE_PRODUCTS_LIST = 50
TELEGRAM_MESSAGE = """
⚠️ Внимание!

Wildberries продает {0} наших товаров по заниженной цене.

Нажмите на пункт в меню, чтобы ознакомиться со списком товаров
"""


@celery_app.task(
    bind=True,
    name=f"app.get_price_products_task",
    default_retry_delay=60 * 60 * 60,
    max_retries=5,
    soft_time_limit=60 * 60 * 60,
    time_limit=60 * 60 * 60,
)
def get_price_products_task(self, products: List[any] = None,
                            max_workers: int = 10):
    proxy_list = get_proxy_list()

    if not products:
        products = []
        products_db = ProductWB.objects.all()
        for s in products_db:
            products.append(
                {"sku": s.sku, "price": s.price, "is_check": s.is_check}
            )
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        products_local = []
        for prod in products:
            products_local.append(
                {
                    "sku": prod.get("sku"),
                    "price": prod.get("price"),
                    "is_check": prod.get("is_check")
                }
            )
            if len(products_local) == SIZE_PRODUCTS_LIST:
                ex.submit(get_price_products, products_local, proxy_list)
                products_local = []
        ex.submit(get_price_products, products_local, proxy_list)

    products_db = ProductWB.objects.filter(
        percentage__gt=settings.PERCENTAGE_MAX
    ).filter(is_check=True)
    products_list = []
    for p in products_db:
        obj = {
            "sku": p.sku,
            "date_updated": p.date_updated
        }
        if obj not in products_list:
            products_list.append(obj)
    count_products = len(products_list)
    if count_products != 0:
        count_requests = 0
        while True:
            if count_requests > 10:
                break
            response = send_message_to_telegram(
                message=TELEGRAM_MESSAGE.format(count_products)
            )
            if response.status_code == 200:
                break
            count_requests += 1


@celery_app.task(
    bind=True,
    name=f"app.get_content_products_task",
    default_retry_delay=60 * 60 * 60,
    max_retries=5,
    soft_time_limit=60 * 60 * 60,
    time_limit=60 * 60 * 60,
)
def get_content_products_task(self, max_workers: int = 10):
    proxy_list = get_proxy_list()
    products_db = ProductWB.objects.all().prefetch_related("specs_set")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        products = []
        for p in products_db:
            products.append(p)
            if len(products) == 200:
                ex.submit(get_content_products, products, proxy_list)
                products = []
        ex.submit(get_content_products, products, proxy_list)


@celery_app.task(
    bind=True,
    name=f"app.get_feedbacks_product_task",
    default_retry_delay=60 * 60 * 60,
    max_retries=5,
    soft_time_limit=60 * 60 * 60,
    time_limit=60 * 60 * 60,
)
def get_feedbacks_product_task(self, max_workers: int = 10):
    proxy_list = get_proxy_list()
    products_db = ProductWB.objects.all().prefetch_related("feedbacks_set")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        products = []
        for p in products_db:
            products.append(p)
            if len(products) == 200:
                ex.submit(get_feedbacks_product, products, proxy_list)
                products = []
        ex.submit(get_feedbacks_product, products, proxy_list)


@celery_app.task(
    bind=True,
    name=f"app.check_price_product_task",
    default_retry_delay=60 * 60 * 60,
    max_retries=5,
    soft_time_limit=60 * 60 * 60,
    time_limit=60 * 60 * 60,
)
def check_price_product_task(self):
    products_db = ProductWB.objects.filter(
        percentage__gt=settings.PERCENTAGE_MAX
    ).filter(is_check=True)
    products_list = []
    for p in products_db:
        obj = {
            "sku": p.sku,
            "date_updated": p.date_updated
        }
        if obj not in products_list:
            products_list.append(obj)
    count_products = len(products_list)
    if count_products != 0:
        count_requests = 0
        while True:
            if count_requests > 10:
                break
            response = send_message_to_telegram(
                message=TELEGRAM_MESSAGE.format(count_products)
            )
            if response.status_code == 200:
                break
            count_requests += 1
    return count_products
