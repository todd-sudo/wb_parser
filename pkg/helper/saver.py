import datetime
from typing import Union

from pytz import timezone
from django.db.utils import IntegrityError

from app.models import (
    ProductWB, Specification, Feedback, Product1C, PriceHistory,
)
from pkg.helper.logic import calculate_percentage_of_prices


def save_price_history(product_wb: ProductWB, price: int) -> PriceHistory:
    price_history = PriceHistory.objects.create(
        product_wb=product_wb,
        price=price,
        create_at=datetime.date.today()
    )
    return price_history


def save_product_price(
    sku: str,
    is_check: bool,
    root_id: str,
    name: str = "",
    price: int = 0,
    is_active: bool = True,
    brand: str = "",
    basic_sale: int = 0,
    basic_price: int = 0,
    client_sale: int = 0,
    client_price: int = 0,
    avg_price: int = 0,
    rating: int = 0,
    sale: int = 0,
    feedbacks: int = 0,
    price_no_sale: int = 0,
    count_in_stock: int = 0,
    price_from_1c: Union[int, float] = 0.0,
):
    tz = timezone('Europe/Moscow')
    datetime_now = datetime.datetime.now(tz=tz)
    url = f"https://www.wildberries.ru/catalog/{sku}/detail.aspx"

    percentage = calculate_percentage_of_prices(
        price_wb=price,
        price_1c=price_from_1c
    )
    print(f"percentage={percentage}")

    product_1c = save_product_1c(
        sku=sku,
        price=price_from_1c,
    )

    try:
        product = ProductWB.objects.create(
            product_1c=product_1c,
            sku=sku,
            is_check=is_check,
            root_id=root_id,
            name=name,
            brand=brand,
            basic_sale=basic_sale,
            basic_price=basic_price,
            sale=sale,
            client_sale=client_sale,
            client_price=client_price,
            price=price,
            price_no_sale=price_no_sale,
            avg_price=avg_price,
            rating=rating,
            feedbacks=feedbacks,
            count_in_stock=count_in_stock,
            count_in_stock_old=count_in_stock,
            is_active=is_active,
            date_updated=datetime_now,
            url=url,
            percentage=percentage,
        )
        price_history = save_price_history(product, price)
        print(price_history)
    except IntegrityError:
        product = ProductWB.objects.get(sku=sku)

        product.product_1c = product_1c
        product.root_id = root_id
        product.is_check = is_check
        product.name = name
        product.brand = brand
        product.basic_sale = basic_sale
        product.basic_price = basic_price
        product.sale = sale
        product.client_sale = client_sale
        product.client_price = client_price
        product.price = price
        product.price_no_sale = price_no_sale
        product.avg_price = avg_price
        product.rating = rating
        product.feedbacks = feedbacks
        product.count_in_stock = count_in_stock
        product.count_in_stock_old = count_in_stock
        product.is_active = is_active
        product.date_updated = datetime_now
        product.url = url
        product.percentage = percentage

        product.save()

        price_history = save_price_history(product, price)
        print(price_history)

    return product


def save_product_content(
    product: ProductWB,
    sku: str = "",
    description: str = "",
    country: str = "",
    name: str = "",
    url: str = ""
):
    """ Сохраняет контент товара
    """
    product.sku = sku
    product.description = description
    product.country = country
    product.name = name
    product.url = url
    product.save()
    return product


def save_specification(product: ProductWB, name: str, value: str):
    spec = Specification.objects.create(
        product=product,
        name=name,
        value=value
    )
    return spec


def save_feedback(
    product: ProductWB,
    color: str,
    size: str,
    username: str,
    text: str,
    answer: str,
    create_at: str
):
    feedback = Feedback.objects.create(
        product=product,
        color=color,
        size=size,
        username=username,
        text=text,
        answer=answer,
        create_at=create_at,
    )
    return feedback


def save_product_1c(sku: str, price: int):
    try:
        product_1c = Product1C.objects.create(
            sku=sku,
            price=price,
            date_updated=datetime.date.today()
        )
    except IntegrityError:
        product_1c = Product1C.objects.get(sku=sku)
        product_1c.sku = sku
        product_1c.price = price
        product_1c.date_updated = datetime.date.today()
        product_1c.save()
    return product_1c
