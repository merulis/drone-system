from celery import shared_task

from app.core.settings import settings

from app.gonets.repositories.repository import (
    get_gonets_repository,
)

from app.gonets import get_gonets_info
from app.gonets import GonetsMessage


@shared_task
def task_get_message_from_gonets():
    remote_driver_url = str(settings.GONETS.REMOTE_DRIVER_URL)
    result = get_gonets_info(remote_driver_url)
    gonets_messages = [GonetsMessage(**obj) for obj in result]

    repo = get_gonets_repository()
    messages = repo.create_many(gonets_messages)

    return messages
