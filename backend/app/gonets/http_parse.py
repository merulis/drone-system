from requests import Session

from app.core.settings import settings


def get_messages(cookies, user_id):
    with Session() as session:
        url = settings.GONETS.BASE_URL + settings.GONETS.LIST_MESSAGE_ROUTE

        json = settings.GONETS.LIST_MESSAGE_JSON
        json[settings.GONETS.LIST_MESSAGE_USER_ID] = user_id

        with session.post(
            url=url,
            cookies=cookies,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json; charset=utf-8,",
            },
            json=json,
        ) as response:
            response.encoding = "utf-8"
            status = response.status_code
            message_json = response.json()

        return status, message_json