"""cdek."""
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import Response, status, HTTPException, Depends, APIRouter

from app.config import settings

from app.schemas import EmailCallbackIn

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


@router.post('/v1/email_callback')
async def email_callback(data: EmailCallbackIn):
    """Send an email."""

    body = """
    <style>
        .btn-link {
        text-decoration: underline;
        color: #0069c2;
        }
        .title {
            margin-bottom: 10px;
        }
        .block {
            margin-bottom: 3px;
        }
    </style>
    <h3 class="title">Запрос на обратный звонок.</h3>
    <div class="block">Имя: %s</div>
    <div>Телефон: <a href="tel:%s">%s</a></div>
    """ % (data.name, data.phone, data.phone)

    status_code = send_email(
        settings.email_from,
        settings.email_pwd,
        settings.email_to,
        "Обратный звонок",
        body,
        'html'
    )

    if status_code != 200:
        raise HTTPException(
            status_code=status_code,
            detail="Что то пошло не так. Попробуйте снова через несколько минут."
        )

    return Response(status_code=200, content='')
