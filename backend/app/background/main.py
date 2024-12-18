from celery import Celery

from app.core.settings import settings


celery = Celery("background", broker=str(settings.CELERY.BROCKER_URL))

celery.autodiscover_tasks(["tasks"])
