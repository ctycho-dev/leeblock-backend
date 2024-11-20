"""cdek."""
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import Response, status, HTTPException, Depends, APIRouter

from app.config import settings

from app.schemas import EmailIn

router = APIRouter(tags=['Email'])


def send_email(
        email_from: str,
        email_pwd: str,
        email_to: str,
        subject: str,
        body: str,
        body_type: str
) -> int:
    # Set up the email server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create the email
    message = MIMEMultipart()
    message["From"] = email_from
    message["To"] = email_to
    message["Subject"] = subject
    message.attach(MIMEText(body, body_type))

    try:
        # Connect to the server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(email_from, email_pwd)  # Log in to your account
            server.sendmail(email_from, email_to, message.as_string())

    except Exception as e:
        print(f"An error occurred: {e}")
        return 500

    return 200


@router.post('/v1/send_email')
async def email_callback(data: EmailIn):
    """Send an email."""

    status_code = send_email(
        settings.email_from,
        settings.email_pwd,
        settings.email_to,
        data.subject,
        data.body,
        data.msg_type
    )

    if status_code != 200:
        raise HTTPException(
            status_code=status_code,
            detail="Что то пошло не так. Попробуйте снова через несколько минут."
        )

    return Response(status_code=200, content='')
