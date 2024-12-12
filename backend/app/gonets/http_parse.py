import requests

from datetime import datetime

from app.gonets.models import (
    ListMessageBody,
    ListMessageHeaders,
)
from app.core.settings import settings


def get_result_or_none(response: requests.Response) -> list[dict] | None:
    json = response.json()
    data = json.get("d")
    result = data.get("Result")
    if result == "OK":
        records = data.get("Records")
        return records
    return None


def get_list_messages(
    cookies: dict,
    uid: int | str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> list[dict] | None:
    if date_from:
        date_from = date_from.strftime("%d.%m.%Y")

    if date_to:
        date_to = date_to.strftime("%d.%m.%Y")

    with requests.Session() as session:
        url = settings.GONETS.BASE_URL + settings.GONETS.LIST_MESSAGE_ROUTE

        body = ListMessageBody(
            uid=str(uid),
            date_from=date_from,
            date_to=date_to,
        ).model_dump()
        headers = ListMessageHeaders().model_dump()

        with session.post(
            url=url,
            cookies=cookies,
            headers=headers,
            json=body,
        ) as response:
            response.encoding = "utf-8"
            messages = get_result_or_none(response)

        return messages
