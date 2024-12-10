from celery import Celery
from celery.schedules import crontab

from app.core.settings import settings
from app.gonets.main import get_gonets_info


celery = Celery("task", broker=str(settings.CELERY.BROCKER_URL))
remote_driver_url = str(settings.GONETS.REMOTE_DRIVER_URL)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/5"),
        get_message_from_gonets.s(remote_driver_url),
        name="get every 5 minutes",
    )


@celery.task
def get_message_from_gonets(url):
    result = get_gonets_info(url)

    return result
