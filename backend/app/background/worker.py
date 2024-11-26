from celery import Celery
from celery.schedules import crontab

from app.core.settings import settings
from app.gonets.parser import parse_message


celery = Celery("task", broker=str(settings.CELERY.BROCKER_URL))


@celery.task
async def get_message_from_gonets():
    result = await parse_message()

    return result


celery.conf.beat_schedule = {
    "every-5-minutes": {
        "task": "tasks.add",
        "schedule": crontab(minute="*/5"),
    }
}
