from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.schemas.users import UserCreate, UserOut, Token
from app.repositories.user_repository import UserRepository
from app.utils import oauth2
from app.dependencies.factory import DependencyFactory
from app.core.logger import get_logger
from app.dependencies.injection import get_factory


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

logger = get_logger()


@router.get("/", response_model=List[UserOut])
async def get_users(factory: DependencyFactory = Depends(get_factory)):
    """Retrieve all users"""
    try:
        user_repo = UserRepository(factory.db)
        users = await user_repo.get_all()
        return users
    except Exception as exc:
        logger.error('get: /users %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.get("/{user_id}", response_model=List[UserOut])
async def get_user(
    user_id: int,
    factory: DependencyFactory = Depends(get_factory)
):
    """Retrieve user by id"""
    try:
        user_repo = UserRepository(factory.db)
        user = await user_repo.get_by_id(user_id)
        return user
    except Exception as exc:
        logger.error('get: /users/%s %s', user_id, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
    user: UserCreate,
    factory: DependencyFactory = Depends(get_factory)
):
    """Create a new user"""
    try:
        user_repo = UserRepository(factory.db)
        new_user = await user_repo.create_user(user)
        return new_user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc
        ) from exc
    except Exception as exc:
        logger.error('post: /users %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.post('/login', response_model=Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    factory: DependencyFactory = Depends(get_factory),
):
    """
    Login route that uses OAuth2PasswordRequestForm for user login.
    """
    user_repo = UserRepository(factory.db)
    user = await user_repo.get_by_username(user_credentials.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not found')
    
    verified = oauth2.verify_pwd(user_credentials.password, user.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
