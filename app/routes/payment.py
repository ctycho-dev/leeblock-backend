from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import hashlib
import httpx
import json

from app.core.config import settings
from app.db.database import get_db
from app.schemas.payment import CheckoutIn
from app.models.request import Request
from app.services.payment_service import PaymentService
from app.repositories.request_repository import RequestRepository
from app.dependencies.factory import DependencyFactory
from app.core.logger import get_logger
from app.dependencies.injection import get_factory

router = APIRouter(
    prefix='/payments',
    tags=['Payment']
)

logger = get_logger()


@router.post('/')
async def init_payment(
    data: CheckoutIn,
    factory: DependencyFactory = Depends(get_factory)
):
    """Init payment."""
    try:
        request_repo = RequestRepository(factory.db)
        payment_service = PaymentService()

        items = [x.model_dump() for x in data.Receipt.Items]

        # Create a dictionary with the required fields
        request_data = {
            "amount": data.Amount,
            "bug": json.dumps(items),
            "city": data.city,
            "zip": data.zip,
            "address": data.address,
            "first_name": data.first_name,
            "last_name": data.last_name,
            "phone": data.phone,
            "email": data.email,
        }

        # Add promo_code_id only if it is provided
        if hasattr(data, 'promo_code_id') and data.promo_code_id is not None:
            request_data["promo_code_id"] = data.promo_code_id

        # Create the Request object using the dictionary
        request = Request(**request_data)

        request = await request_repo.add(request)
        if not request:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not create a request')

        # Generate the SHA-256 token
        sha256_hash = payment_service.generate_token(data, request.id)

        # Call Tinkoff API to initiate payment
        response = await payment_service.call_tinkoff_api(data, request.id, sha256_hash)

        result = response.json()

        request.token = sha256_hash
        request.payment_id = result['PaymentId']
        await request_repo.update(request)

        return result
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {exc}"
        ) from exc


@router.post('v1/get_payment_status/{order_id}')
async def get_payment_status(order_id: int, db: Session = Depends(get_db)):
    """Init payment."""
    result = None

    try:
        row = db.query(Request).filter(Request.id == order_id).first()
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
