import ssl, smtplib
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger()


class EmailService:
    """Service for sending emails."""

    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_from = settings.email_from
        self.email_pwd = settings.email_pwd

    def send_email(self, email_to: str, subject: str, body: str, body_type: str = "plain") -> int:
        """Send an email with the provided details."""
        message = MIMEMultipart()
        message["From"] = self.email_from
        message["To"] = email_to
        message["Subject"] = subject
        message.attach(MIMEText(body, body_type))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.email_from, self.email_pwd)
                server.sendmail(self.email_from, email_to, message.as_string())
            return 200

        except Exception as exc:
            logger.error("Failed to send email to %s: %s", email_to, exc)
            return 500

    # async def send_email(self, email_to, subject, body, body_type="plain"):
    #     """Send an email securely using SMTP with proper SSL/TLS handling."""
    #     # Create the email message
    #     message = MIMEMultipart()
    #     message["From"] = self.email_from
    #     message["To"] = email_to
    #     message["Subject"] = subject
    #     message.attach(MIMEText(body, body_type))

    #     try:
    #         # Use a secure SSL context
    #         ssl_context = ssl.create_default_context()

    #         # Connect to the SMTP server asynchronously
    #         async with SMTP(
    #             hostname=self.smtp_server,
    #             port=self.smtp_port,
    #             use_tls=False,  # For StartTLS
    #             tls_context=ssl_context,
    #         ) as server:
    #             # Initiate StartTLS
    #             await server.starttls()
    #             # Authenticate with the SMTP server
    #             await server.login(self.email_from, self.email_pwd)
    #             # Send the email
    #             await server.send_message(message)

    #         return 200
    #     except Exception as exc:
    #         logger.error("Failed to send email to %s: %s", email_to, exc)
    #         return 500
