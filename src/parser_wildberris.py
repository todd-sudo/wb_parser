
import time
import json

from services import get_new_json, write_state_parser
from logger import logger


@logger.catch()
def wb_parser(data_json):
    """Парсер wildberries"""
    data = []
    index = 1
    counter = 0

    for row in data_json['id']:
        data_json = json.loads(get_new_json(row))
        try:
            sale = data_json['data']['products'][0]['sale']
        except KeyError:
            sale = ''
        try:
            price = data_json['data']['products'][0]['priceU']
            price = price / 100
            price = int(price)
        except KeyError:
            price = ''
        try:
            basic_sale = data_json['data']['products'][0]['extended'][
                'basicSale']
        except KeyError:
            basic_sale = ''
        try:
            basic_price = data_json['data']['products'][0]['extended'][
                'basicPriceU']
            basic_price = basic_price / 100
            basic_price = int(basic_price)
        except KeyError:
            basic_price = ''
        try:
            promo_sale = data_json['data']['products'][0]['extended'][
                'promoSale']
        except KeyError:
            promo_sale = ''
        try:
            promo_price = data_json['data']['products'][0]['extended'][
                'promoPriceU']
            promo_price = promo_price / 100
            promo_price = int(promo_price)
        except KeyError:
            promo_price = ''
        try:
            customer_sale = data_json['data']['products'][0]['extended'][
                'clientSale']
        except KeyError:
            customer_sale = ''
        try:
            customer_price = data_json['data']['products'][0]['extended'][
                'clientPriceU']
            customer_price = customer_price / 100
            customer_price = int(customer_price)
        except KeyError:
            customer_price = ''

        output_json = {
            row: {
                'price': price,
                'sale': sale,
                'basicSale': basic_sale,
                'basicPrice': basic_price,
                'promoSale': promo_sale,
                'promoPrice': promo_price,
                'CustomerSale': customer_sale,
                'CustomerPrice': customer_price,
            }
        }
        data.append(output_json)
        counter += 1
        index += 1
        logger.info(f'Выполнено итераций - #{counter}')

        write_state_parser(_state='false')

        time.sleep(2 if index % 10 != 0 else 20)

    with open('results/data_out.json', "a", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        write_state_parser(_state='true')
        logger.info('Success parsing! Goodbye!!! :-)')
