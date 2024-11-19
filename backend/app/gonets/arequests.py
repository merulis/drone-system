from aiohttp import ClientSession
from app.core.settings import settings


async def get_messages(cookies, user_id):
    async with ClientSession(cookies=cookies) as session:
        url = settings.GONETS.BASE_URL + settings.GONETS.LIST_MESSAGE_ROUTE

        json = settings.GONETS.LIST_MESSAGE_JSON
        json[settings.GONETS.LIST_MESSAGE_USER_ID] = user_id

        async with session.post(
            url=url,
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json; charset=utf-8,",
            },
            json=json,
        ) as response:
            status = response.status
            message_json = await response.json()

        return status, message_json
