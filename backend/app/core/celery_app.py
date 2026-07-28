from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "interviewiq",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.tasks.email_tasks",
        "app.tasks.resume_tasks",
        "app.tasks.ai_tasks",
        "app.tasks.interview_tasks",
        "app.tasks.report_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Kolkata",
    enable_utc=False,
    task_track_started=True,
    result_expires=3600,
)