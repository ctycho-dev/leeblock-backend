"""cdek."""
import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import hashlib
import requests
import json

from app.config import settings
from app.database import get_db
from app.schemas import CheckoutIn

from app.models import Products, Requests

from app.config import settings


router = APIRouter(tags=['Database'])


@router.get('/v1/get_products')
async def get_products(db: Session = Depends(get_db),):
    """Send an email."""

    products = db.query(Products).filter(Products.published == 1).order_by(Products.sequence).all()

    return products


@router.get('/v1/get_products/{product_id}')
async def get_product_by_id(product_id: str, db: Session = Depends(get_db),):
    """Send an email."""

    product = db.query(Products).filter(Products.product_id == product_id).first()

    return product


@router.get('/v1/get_products_to_display')
async def get_products_to_display(db: Session = Depends(get_db)):
    """Send an email."""

    products = db.query(Products).filter(Products.display_on_main == 1).all()

    return products


@router.post('/v1/init_payment')
async def init_payment(data: CheckoutIn, db: Session = Depends(get_db)):
    """Init payment."""
    result = None

    try:
        items = [x.dict() for x in data.Receipt.Items]

        request = Requests(
            amount=data.Amount,
            bug=json.dumps(items),
            city=data.city,
            zip=data.zip,
            address=data.address,
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            email=data.email
        )

        db.add(request)
        db.commit()
        db.refresh(request)

        data_for_token = [
            str(data.Amount),  # TerminalKey
            settings.terminal_desc,  # Description
            str(request.id),  # OrderId
            settings.terminal_pwd,  # Password
            settings.terminal_key  # TerminalKey
        ]

        sha256_hash = hashlib.sha256(''.join(data_for_token).encode()).hexdigest()

        init_data = {
            'TerminalKey': settings.terminal_key,
            'Amount': data.Amount,
            'OrderId': request.id,
            'Description': settings.terminal_desc,
            'Token': sha256_hash,
            'DATA': data.DATA.dict(),
            'Receipt': data.Receipt.dict()
        }

        response = requests.post(f'{settings.tinkoff_url}/v2/Init',
                                 headers={'Content-Type': 'application/json'},
                                 json=init_data)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Что то пошло не так. Попробуйте снова через несколько минут."
            )

        result = response.json()

        row = db.query(Requests).filter(Requests.id == request.id).first()

        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Did not find')
        row.token = sha256_hash
        row.payment_id = result['PaymentId']

        db.commit()
        db.refresh(row)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {exc}"
            ) from exc

    return result


@router.post('v1/get_payment_status/{order_id}')
async def get_payment_status(order_id: int, db: Session = Depends(get_db)):
    """Init payment."""
    result = None

    try:
        row = db.query(Requests).filter(Requests.id == order_id).first()
        if row is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Did not find')

        # response = requests.post(f'{settings.tinkoff_url}/v2/GetState',
        #                          headers={'Content-Type': 'application/json'},
        #                          json=init_data)

        # if response.status_code != 200:
        #     raise HTTPException(
        #         status_code=response.status_code,
        #         detail="Что то пошло не так. Попробуйте снова через несколько минут."
        #     )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {exc}"
            ) from exc
    return result
