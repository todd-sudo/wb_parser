from typing import List

from app.models import ProductWB
from pkg.client.client import sync_post, REQUEST_EXCEPTIONS
from pkg.helper.request_retry import request_retry_post
from pkg.helper.saver import save_feedback


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Accept': '*/*',
}


def parse_feedbacks(feedbacks_json: List[dict]) -> List[dict]:
    feedbacks_to_db = []
    for item in feedbacks_json:
        username = ""
        user_detail = item.get("wbUserDetails")
        if user_detail:
            username = user_detail.get("name")
        text = item.get("text")
        color = item.get("color")
        size = item.get("size")
        create_at = item.get("createdDate")
        answer = item.get("answer", "")
        if answer:
            answer = answer.get("text")
        feedbacks_to_db.append({
            "username": username,
            "text": text,
            "color": color,
            "size": size,
            "create_at": create_at,
            "answer": answer
        })
    return feedbacks_to_db


def get_feedbacks_product(products: List[ProductWB], proxy_list: list):
    """ Собирает отзывы на товар
    """
    url = "https://feedbacks.wildberries.ru/api/v1/summary/full"
    for product in products:
        co, deleted = product.feedbacks_set.all().delete()
        print(co, deleted)
        take = 30
        skip = 0
        for _ in range(20):
            json_data = f'{{"imtId":{product.root_id},"take":{take},"skip":{skip}}}'
            try:
                response = sync_post(
                    url=url,
                    headers=headers,
                    data=json_data,
                    proxy_list=proxy_list
                )
 
            except REQUEST_EXCEPTIONS as err:
                print(err)
                response = request_retry_post(
                    url=url, headers=headers, proxy_list=proxy_list, data=json_data
                )
            if response or response.status_code == 200:
                try:
                    res_json = response.json()
                except REQUEST_EXCEPTIONS:
                    continue
            else:
                break
            if not res_json:
                break

            feedbacks_json_list = res_json.get("feedbacks")
            if not feedbacks_json_list:
                break

            feedbacks_to_db = parse_feedbacks(feedbacks_json=feedbacks_json_list)
            for f in feedbacks_to_db:
                feedback = save_feedback(
                    product=product,
                    answer=f.get("answer"),
                    color=f.get("color"),
                    create_at=f.get("create_at"),
                    size=f.get("size"),
                    text=f.get("text"),
                    username=f.get("username")
                )

            skip += 30
            take += 30
