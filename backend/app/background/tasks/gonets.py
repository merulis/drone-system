from celery import shared_task

from app.core.settings import settings
from app.gonets import get_gonets_info


@shared_task
def get_message_from_gonets():
    remote_driver_url = str(settings.GONETS.REMOTE_DRIVER_URL)
    result = get_gonets_info(remote_driver_url)

    return result
