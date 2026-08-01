import resend

from app.core.config import settings

resend.api_key = settings.resend_api_key


class ResendClient:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html: str,
    ):

        resend.Emails.send(
            {
                "from": settings.resend_from,
                "to": [to_email],
                "subject": subject,
                "html": html,
            }
        )