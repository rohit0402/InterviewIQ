import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings


class BrevoClient:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html: str,
    ):

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.brevo_api_key

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        sender = {
            "name": settings.brevo_sender_name,
            "email": settings.brevo_sender_email,
        }

        receiver = [
            {
                "email": to_email,
            }
        ]

        email = sib_api_v3_sdk.SendSmtpEmail(
            sender=sender,
            to=receiver,
            subject=subject,
            html_content=html,
        )

        try:
            api_instance.send_transac_email(email)
        except ApiException as e:
            raise Exception(f"Brevo Email Error: {e}")