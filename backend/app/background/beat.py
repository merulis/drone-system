from .main import celery

from celery.schedules import crontab
from .tasks.gonets import get_message_from_gonets


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/5"),
        get_message_from_gonets.s(),
        name="get every 5 minutes",
    )
