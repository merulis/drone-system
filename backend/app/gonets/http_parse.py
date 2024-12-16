import requests

from datetime import datetime

from app.schemas.gonets import (
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
    uid: int,
    date_from: datetime | str | None = None,
    date_to: datetime | str | None = None,
) -> list[dict] | None:
    if date_from:
        date_from = date_from.strftime("%d.%m.%Y")
    else:
        date_from = ""

    if date_to:
        date_to = date_to.strftime("%d.%m.%Y")
    else:
        date_to = ""

    with requests.Session() as session:
        url = settings.GONETS.BASE_URL + settings.GONETS.LIST_MESSAGE_ROUTE

        body = ListMessageBody(
            uid=str(uid),
            date_from=date_from,
            date_to=date_to,
        ).model_dump(by_alias=True)
        headers = ListMessageHeaders().model_dump(by_alias=True)

        with session.post(
            url=url,
            cookies=cookies,
            headers=headers,
            json=body,
        ) as response:
            response.encoding = "utf-8"

            if not response.status_code == 200:
                raise Exception(msg="Response error, no data in response")

            messages = get_result_or_none(response)

        return messages
