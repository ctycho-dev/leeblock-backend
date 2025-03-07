from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response

from app.models.user import User
from app.models.user import PromoCode
from app.repositories.user_repo import UserRepository
from app.repositories.promo_code_repo import PromoCodeRepository
from app.utils import oauth2
from app.dependencies.factory import DependencyFactory
from app.core.logger import get_logger
from app.schemas.promo_code import PromoCodeCreate
from app.dependencies.injection import get_factory
from app.dependencies.injection import get_current_user
from app.core.config import settings


router = APIRouter(
    prefix='/promo',
    tags=['Promo Codes']
)

logger = get_logger()


@router.get("/",)
async def get_promo(factory: DependencyFactory = Depends(get_factory)):
    """Retrieve all users"""
    try:
        promo_repo = PromoCodeRepository(factory.db)
        promo = await promo_repo.get_all_with_user()
        # promo = await promo_repo.get_all()
        return promo
    except Exception as exc:
        logger.error('get: /users %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.get("/{code}")
async def get_promocode_by_code(
    code: str,
    factory: DependencyFactory = Depends(get_factory)
):
    """
    Retrieve a promo code by its code along with the associated user's email.
    """
    try:
        promo_repo = PromoCodeRepository(factory.db)
        promocode = await promo_repo.get_by_code(code)

        return promocode
    except HTTPException as exc:
        raise exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/")
async def create_promo_code(
    promo_code: PromoCodeCreate,
    _: User = Depends(get_current_user),
    factory: DependencyFactory = Depends(get_factory)
):
    """
    Create a new promo code for the authenticated KOL.

    Args:
        promo_code (PromoCodeCreate): The promo code data.
        db (AsyncSession): The database session.
        current_kol (KolUser): The authenticated KOL user.

    Returns:
        dict: A success message.
    """
    try:
        # if not user['is_verified']:
        #     raise HTTPException(
        #         status_code=status.HTTP_401_UNAUTHORIZED,
        #         detail="User not verified.",
        #         headers={"WWW-Authenticate": "Bearer"},
        #     )

        promo_repo = PromoCodeRepository(factory.db)
        # promos = await promo_repo.get_by_user_id(user['id'])

        # if promos:
        #     raise ValueError('Promocode already exists')

        new_promo = await promo_repo.add(PromoCode(
            code=promo_code.code,
            user_id=promo_code.user_id,
            # user_id=user['id'],
            discount_type=promo_code.discount_type,
            discount_value=promo_code.discount_value,
            valid_until=promo_code.valid_until,
        ))
        return new_promo
    except HTTPException as exc:
        raise exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
