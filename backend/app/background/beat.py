from .main import celery

from celery.schedules import crontab

from app.gonets import task_get_message_from_gonets


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/5"),
        task_get_message_from_gonets.s(),
        name="get every 5 minutes",
    )
