from pathlib import Path

from app.core.config import settings
from app.email.smtp import SMTPClient


class EmailService:

    @staticmethod
    def send_verification_email(
        email: str,
        token: str,
    ):

        template = (
            Path(__file__).parent
            / "templates"
            / "verify_email.html"
        ).read_text(
            encoding="utf-8"
        )

        verification_url = (
            f"{settings.frontend_url}"
            f"/verify-email?token={token}"
        )

        html = template.replace(
            "{{verification_url}}",
            verification_url,
        )

        SMTPClient.send_email(
            to_email=email,
            subject="Verify your InterviewIQ account",
            html=html,
        )

    @staticmethod
    def send_password_reset_email(
        email: str,
        token: str,
    ):

        template = (
            Path(__file__).parent
            / "templates"
            / "reset_password.html"
        ).read_text(
            encoding="utf-8"
        )

        reset_url = (
            f"{settings.frontend_url}"
            f"/reset-password?token={token}"
        )

        html = template.replace(
            "{{reset_url}}",
            reset_url,
        )

        SMTPClient.send_email(
            to_email=email,
            subject="Reset your InterviewIQ password",
            html=html,
        )