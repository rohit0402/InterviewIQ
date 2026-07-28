from app.core.celery_app import celery_app
from app.email.email_service import EmailService
from app.tasks.base import BaseTask

@celery_app.task(
    bind=True,
    base=BaseTask,
)
def send_verification_email_task(
    self,
    email: str,
    token: str,
):
    EmailService.send_verification_email(
        email=email,
        token=token,
    )


@celery_app.task(
    bind=True,
    base=BaseTask,
)
def send_password_reset_email_task(
    self,
    email: str,
    token: str,
):
    EmailService.send_password_reset_email(
        email=email,
        token=token,
    )