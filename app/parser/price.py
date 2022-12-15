import json
from typing import List, Union

from pkg.client.client import sync_get, REQUEST_EXCEPTIONS
from pkg.helper.request_retry import request_retry
from pkg.helper.saver import save_product_price


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) '
                  'Gecko/20100101 Firefox/104.0',
    'Accept': '*/*',
}


def parse_objects_price(product_json: dict) -> dict:
    """ Распаршевает товары из json
    """
    item = product_json
    sku = item.get("id")
    if not sku:
        return {}
    root_id = item.get("root")
    if root_id:
        root_id = str(root_id)
    else:
        return {}
    price_no_sale = item.get("priceU", 0)
    if price_no_sale != 0:
        price_no_sale = price_no_sale / 100
    sale = item.get("sale", 0)
    price = item.get("salePriceU", 0)
    if price != 0:
        price = price / 100
    name = item.get("name")
    brand = item.get("brand")

    basic_sale, basic_price, client_sale, client_price = 0, 0, 0, 0
    e = item.get("extended")
    if e:
        basic_sale = e.get("basicSale", 0)
        basic_price = e.get("basicPriceU", 0)
        if basic_price != 0:
            basic_price = basic_price / 100
        client_sale = e.get("clientSale", 0)
        client_price = e.get("clientPriceU", 0)
        if client_price != 0:
            client_price = client_price / 100
    avg_price = item.get("averagePrice", 0)
    if avg_price != 0:
        avg_price = avg_price / 100
    rating = item.get("rating", 0)
    feedbacks = item.get("feedbacks")

    count_in_stock = 0
    sizes = item.get("sizes")
    if sizes:
        for size in sizes:
            stocks = size.get("stocks")
            if stocks:
                for stock in stocks:
                    qty = stock.get("qty", 0)
                    count_in_stock += qty
    is_active = True
    if count_in_stock == 0:
        is_active = False
    obj = {
        "sku": sku,
        "price_no_sale": price_no_sale,
        "sale": sale,
        "price": price,
        "basic_sale": basic_sale,
        "basic_price": basic_price,
        "client_sale": client_sale,
        "client_price": client_price,
        "avg_price": avg_price,
        "rating": rating,
        "feedbacks": feedbacks,
        "count_in_stock": count_in_stock,
        "is_active": is_active,
        "name": name,
        "brand": brand,
        "root_id": root_id
    }
    return obj


def save_price_products(
        parse_object: dict, price_from_1c: Union[int, float], is_check: bool
) -> int:
    if not parse_object:
        return 0
    obj = parse_object
    product = save_product_price(
        sku=obj.get("sku"),
        root_id=obj.get("root_id"),
        price_no_sale=obj.get("price_no_sale"),
        sale=obj.get("sale"),
        price=obj.get("price"),
        basic_sale=obj.get("basic_sale"),
        basic_price=obj.get("basic_price"),
        client_sale=obj.get("client_sale"),
        client_price=obj.get("client_price"),
        avg_price=obj.get("avg_price"),
        rating=obj.get("rating"),
        feedbacks=obj.get("feedbacks"),
        count_in_stock=obj.get("count_in_stock"),
        is_active=obj.get("is_active"),
        name=obj.get("name"),
        brand=obj.get("brand"),
        price_from_1c=price_from_1c,
        is_check=is_check
    )
    print(product)
    return 1


def get_price_products(
        products: List[any], proxy_list: List[str] = None, save: bool = True
) -> int:
    """ Получение товаров по списку кодов
    """
    count = 0
    for product in products:
        url = f'https://card.wb.ru/cards/detail?spp=26&regions=80,68,64,83,' \
            f'4,38,33,82,86,30,40,48,1,22,66,31&pricemarginCoeff=1.0&reg=1' \
            f'&appType=1&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=3,6,19,21,8' \
            f'&sppFixGeo=4&dest=-1059500,-72639,-3826860,-5551777&nm={product.get("sku")}'
        data = None

        price_from_1c = product.get("price", 0.0)
        is_check = product.get("is_check")
        print(f"is_check = {is_check}")
        try:
            response = sync_get(url=url, headers=headers, proxy_list=proxy_list)
        except REQUEST_EXCEPTIONS as err:
            print(err)
            response = request_retry(url=url, headers=headers, proxy_list=proxy_list)
        if response:
            try:
                data = json.loads(response.content, strict=False)
            except REQUEST_EXCEPTIONS:
                return 0
        if not data:
            return 0
        data = data.get("data")
        if not data:
            return 0
        products_json = data.get("products")
        if not products_json:
            return 0
        product_json = products_json[0]
        parse_object: dict = parse_objects_price(product_json=product_json)
        if save:
            count += save_price_products(parse_object, price_from_1c, is_check)
    return count



