"""cdek."""
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import Response, status, HTTPException, Depends, APIRouter

from app.core.config import settings
from app.schemas.email import EmailIn
from app.services.email_service import EmailService
from app.dependencies.injection import get_email_service

router = APIRouter(
    prefix='/email',
    tags=['Email']
)


@router.post('/')
def email_callback(
    data: EmailIn,
    email_service: EmailService = Depends(get_email_service)
):
    """Send an email using the email service."""
    status_code = email_service.send_email(
        email_to=settings.email_to,
        subject=data.subject,
        body=data.body,
        body_type=data.msg_type
    )

    if status_code != 200:
        raise HTTPException(
            status_code=status_code,
            detail="Что-то пошло не так. Попробуйте снова через несколько минут."
        )

    return Response(status_code=200)
