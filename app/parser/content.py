"""
https://wbx-content-v2.wbstatic.net/ru/61764985.json
"""
import json
from typing import List
from app.models import ProductWB

from pkg.client.client import REQUEST_EXCEPTIONS, sync_get
from pkg.helper.request_retry import request_retry
from pkg.helper.saver import save_product_content, save_specification


def parse_object_content(item: dict) -> dict:
    sku = item.get("nm_id")
    name = item.get("imt_name")
    if name == "" or name is None:
        name = item.get("subj_name")
    description = item.get("description")
    url = f"https://www.wildberries.ru/catalog/{sku}/detail.aspx"
    specs = []
    country = ""
    options = item.get("options")
    if options:
        for i in options:
            if "Страна производства" in i.get("value"):
                country = i.get("value")
            specs.append(
                {"name": i.get("name"), "value": i.get("value")}
            )
    brand = ""
    selling = item.get("selling")
    if selling:
        brand = selling.get("brand_name")
    return {
        "sku": sku,
        "name": name,
        "description": description,
        "country": country,
        "brand": brand,
        "url": url,
        "specs": specs,
    }


def get_content_products(products: List[ProductWB], proxy_list: list):
    """ Парсинг контента у товара
    """
    for product_db in products:
        co, deleted = product_db.specs_set.all().delete()
        print(co, deleted)
        data = None
        url = f"https://wbx-content-v2.wbstatic.net/ru/{product_db.sku}.json"
        try:
            response = sync_get(url=url, proxy_list=proxy_list)
        except REQUEST_EXCEPTIONS as err:
            print(err)
            response = request_retry(url=url, proxy_list=proxy_list)
        if response:
            try:
                data = json.loads(response.content, strict=False)
            except REQUEST_EXCEPTIONS:
                continue
        if not data:
            return 0
        obj = parse_object_content(data)
        product = save_product_content(
            product=product_db,
            sku=product_db.sku,
            description=obj.get("description"),
            country=obj.get("country"),
            name=obj.get("name"),
            url=obj.get("url")
        )
        specs = obj.get("specs")
        if specs:
            for s in specs:
                spec_db = save_specification(
                    product=product,
                    name=s.get("name"),
                    value=s.get("value"),
                )
