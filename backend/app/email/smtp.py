import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class SMTPClient:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html: str,
    ):
        message = MIMEMultipart("alternative")

        message["Subject"] = subject
        message["From"] = settings.smtp_from_email
        message["To"] = to_email

        message.attach(
            MIMEText(html, "html")
        )

        with smtplib.SMTP_SSL(
            settings.smtp_host,
            settings.smtp_port,
        ) as server:

            server.login(
                settings.smtp_username,
                settings.smtp_password,
            )

            server.sendmail(
                settings.smtp_from_email,
                to_email,
                message.as_string(),
            )