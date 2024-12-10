import requests

from app.gonets.models import (
    ListMessageBody,
    ListMessageHeaders,
    custom_adict,
)
from app.core.settings import settings


def get_result_or_none(response: requests.Response) -> list[dict]:
    json = response.json()
    print(json)
    data = json.get("d")
    result = data.get("Result")
    if result == "OK":
        records = data.get("Records")
        return records
    return None


def get_list_messages(cookies, user_id):
    with requests.Session() as session:
        url = settings.GONETS.BASE_URL + settings.GONETS.LIST_MESSAGE_ROUTE

        body = custom_adict(ListMessageBody(uid=str(user_id)))
        headers = custom_adict(ListMessageHeaders())

        print(body)
        print(headers)

        with session.post(
            url=url,
            cookies=cookies,
            headers=headers,
            json=body,
        ) as response:
            response.encoding = "utf-8"
            messages = get_result_or_none(response)

        return messages
