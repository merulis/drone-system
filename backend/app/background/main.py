from celery import Celery

from app.core.settings import settings


celery = Celery(
    main="background",
    broker=str(settings.CELERY.BROCKER_URL),
)

celery.autodiscover_tasks()
