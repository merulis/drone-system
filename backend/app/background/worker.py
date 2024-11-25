from celery import Celery

from app.core.settings import settings
from app.gonets.parser import parse_message


celery = Celery("task", broker=settings.CELERY.BROCKER_URL)


@celery.task
async def get_message_from_gonets():
    result = await parse_message()

    return result
