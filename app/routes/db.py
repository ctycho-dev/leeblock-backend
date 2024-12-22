import time
from fastapi import status, HTTPException, Depends, APIRouter, Response, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import hashlib
import requests
import json
from typing import List

from app.config.config import settings
from app.database import get_db
from app.schemas import CheckoutIn, ProductResponse
from app.models import Products, Requests
from app.redis_client import get_redis_client
from app.config.logger import get_logger


router = APIRouter(tags=['Database'])
logger = get_logger()


# @router.get('/v1/get_products', response_model=List[ProductResponse])
@router.get('/v1/get_products')
async def get_products(
    db: Session = Depends(get_db),
    rc: Session = Depends(get_redis_client)
):
    """
    Fetch all published products, ordered by sequence.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[ProductResponse]: A list of all published products.

    Raises:
        HTTPException: If no products are found.
    """
    try:
        cached_products = rc.get('products')
        if cached_products:
            return json.loads(cached_products)

        products = db.query(Products).filter(Products.published == 1).order_by(Products.sequence).all()
        if not products:
            raise HTTPException(
                status_code=404,
                detail="No published products found."
            )

        # Convert products into a list of dictionaries as expected by the response model
        product_list = [ProductResponse.model_validate(product).model_dump() for product in products]

        # Cache the list of products
        rc.set('products', json.dumps(product_list), ex=3600)

        return product_list  # Return the transformed product list
    except Exception as exc:
        logger.error('/v1/get_products %s', exc)
        raise HTTPException(
            status_code=500,
            detail=exc
        ) from exc


@router.get('/v1/get_products/{product_id}', response_model=ProductResponse)
async def get_product_by_id(
    product_id: str,
    db: Session = Depends(get_db),
    rc: Session = Depends(get_redis_client)
):
    """
    Fetch a product by its ID.

    Args:
        product_id (str): The ID of the product to retrieve.
        db (Session): The database session dependency.

    Returns:
        ProductResponse: Details of the requested product.

    Raises:
        HTTPException: If the product is not found.
    """
    try:
        cached_product = rc.get(product_id)
        if cached_product:
            return json.loads(cached_product)

        product = db.query(Products).filter(Products.product_id == product_id).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product with ID '{product_id}' not found."
            )

        product_json = ProductResponse.model_validate(product).model_dump()

        rc.set(product_id, json.dumps(product_json), ex=3600)
        return product_json
    except Exception as exc:
        logger.error('/v1/get_products/product_id %s', exc)
        raise HTTPException(
            status_code=500,
            detail=exc
        ) from exc



@router.get('/v1/get_products_to_display', response_model=list[ProductResponse])
async def get_products_to_display(
    db: Session = Depends(get_db),
    rc: Session = Depends(get_redis_client)
):
    """
    Fetch all products marked for display on the main page.

    Args:
        db (Session): The database session dependency.

    Returns:
        List[ProductResponse]: A list of products to display on the main page.

    Raises:
        HTTPException: If no products are found for display.
    """
    try:
        cached_products = rc.get('products_to_display')
        if cached_products:
            return json.loads(cached_products)
        
        products = db.query(Products).filter(Products.display_on_main == 1).all()

        if not products:
            raise HTTPException(
                status_code=404,
                detail="No products to display on the main page."
            )

        product_list = [ProductResponse.model_validate(product).model_dump() for product in products]
        rc.set('products_to_display', json.dumps(product_list), ex=3600)
        return product_list
    except Exception as exc:
        logger.error('/v1/get_products_to_display %s', exc)
        raise HTTPException(
            status_code=500,
            detail=exc
        ) from exc



@router.post('/v1/init_payment')
async def init_payment(data: CheckoutIn, db: Session = Depends(get_db)):
    """Init payment."""
    result = None

    try:
        items = [x.model_dump() for x in data.Receipt.Items]

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
                                 json=init_data,
                                 timeout=30)

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
        logger.error('/v1/init_payment %s', exc)
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

        # Here you would typically call a payment provider API to get the payment status
        # response = requests.post(f'{settings.tinkoff_url}/v2/GetState',
        #                          headers={'Content-Type': 'application/json'},
        #                          json=init_data)

        # if response.status_code != 200:
        #     raise HTTPException(
        #         status_code=response.status_code,
        #         detail="Что то пошло не так. Попробуйте снова через несколько минут."
        #     )

    except Exception as exc:
        logger.error('/v1/get_payment_status %s', exc)
        raise HTTPException(
            status_code=500,
            detail=f"Error: {exc}"
        ) from exc

    return result
