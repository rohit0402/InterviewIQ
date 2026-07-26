from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "interviewiq",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=False,

    # Recommended settings
    task_track_started=True,
    result_expires=3600,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(
    ["app.tasks"]
)