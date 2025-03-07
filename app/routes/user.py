from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse

from app.schemas.users import UserCreate
from app.schemas.users import UserUpdate
from app.schemas.users import UserUpdatePassword
from app.schemas.users import UserOut
from app.schemas.users import Token
from app.models.user import User
from app.models.user import PromoCode
from app.repositories.user_repo import UserRepository
from app.repositories.promo_code_repo import PromoCodeRepository
from app.utils import oauth2
from app.dependencies.factory import DependencyFactory
from app.services.email_service import EmailService
from app.core.logger import get_logger
from app.schemas.promo_code import PromoCodeCreate
from app.dependencies.injection import get_factory
from app.dependencies.injection import get_current_user
from app.core.config import settings


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

logger = get_logger()


def send_verification_email(
    email: str,
    token: str,
):
    """
    Send a verification email to the user.

    Args:
        email (str): The recipient's email address.
        token (str): The verification token.
    """
    verification_url = f"{settings.frontend_url}/verify/{token}"
    subject = "Verify Your Email Address"
    body = f"""
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Verification</title>
        </head>
        <body>
            <div>
                <h2 style="color: #000; margin-bottom: 10px;">Email Verification</h2>
                <p style="color: #000; margin-bottom: 10px;">Please click the link below to verify your email address:</p>
                <a href="{verification_url}">Verify Email</a>
            </div>
        </body>
        </html>
    """

    email_service = EmailService()
    email_service.send_email(email, subject, body, 'html')


@router.get("/", response_model=list[UserOut])
async def get_users(factory: DependencyFactory = Depends(get_factory)):
    """Retrieve all users"""
    try:
        user_repo = UserRepository(factory.db)
        users = await user_repo.get_all_non_admin_users()
        # users = await user_repo.get_all()
        return users
    except Exception as exc:
        logger.error('get: /users %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.get("/{user_id}", response_model=UserOut)
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
        print(user)
        user_repo = UserRepository(factory.db)
        new_user = await user_repo.create_user(user)

        # Send verification email
        # token = oauth2.generate_verification_token(new_user.email)
        # send_verification_email(new_user.email, token)
        return new_user
    except ValueError:
        return Response(status_code=status.HTTP_409_CONFLICT)
    except Exception as exc:
        logger.error('post: /users %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.patch("/", status_code=200)
async def update_user(
    upd_user: UserUpdate,
    user: User = Depends(get_current_user),
    factory: DependencyFactory = Depends(get_factory)
):
    """Create a new user"""
    try:
        user_repo = UserRepository(factory.db)

        user.first_name = upd_user.first_name
        user.last_name = upd_user.last_name
        user.phone = upd_user.phone
        await user_repo.update(user)
    except ValueError:
        return Response(status_code=status.HTTP_409_CONFLICT)
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
    user = await user_repo.get_by_email(user_credentials.username)
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content='Not exists.')
    if not user.admin:
        return Response(status_code=status.HTTP_403_FORBIDDEN, content='Forbidden.')
    
    verified = oauth2.verify_password(user_credentials.password, user.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post('/verify', response_model=UserOut)
async def verify(
    user: User = Depends(get_current_user),
):
    """
    Verify the current user's authentication status.

    Args:
        _ (str): Dependency injection for the current authenticated user.

    Returns:
        Response: HTTP 200 OK if the user is authenticated.
    """
    return UserOut.model_validate(user).model_dump()
    # return Response(status_code=200)


@router.post("/send-verification-email", status_code=200)
async def verification_email(
    user: User = Depends(get_current_user),
):
    """Create a new user"""
    try:
        token = oauth2.generate_verification_token(user.email)
        send_verification_email(user.email, token)
    except ValueError:
        return Response(status_code=status.HTTP_409_CONFLICT)
    except Exception as exc:
        logger.error('post: /users %s', exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request."
        ) from exc


@router.get("/verify-email/{token}", response_class=HTMLResponse)
async def verify_email(
    token: str,
    factory: DependencyFactory = Depends(get_factory)
):
    """
    Verify a KOL's email address using the verification token.

    Args:
        token (str): The verification token.
        db (AsyncSession): The database session.

    Returns:
        dict: A success or error message.
    """
    try:
        user_repo = UserRepository(factory.db)

        email = oauth2.decode_email_token(token)
        await user_repo.verify_user(email)
        html_content = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Email Verified</title>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        font-family: Arial, sans-serif;
                        background-color: #f9fafb;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                    }
                    .container {
                        text-align: center;
                        padding: 16px;
                    }
                    .message {
                        font-weight: bold;
                        font-size: 1.25rem;
                        margin-bottom: 1rem;
                        color: #1f2937;
                    }
                    .home-link {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        gap: 0.75rem;
                        background-color: #4f46e5;
                        color: white;
                        padding: 0.5rem 1rem;
                        border-radius: 0.375rem;
                        text-decoration: none;
                        font-size: 0.875rem;
                        font-weight: 600;
                        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
                        transition: background-color 0.2s;
                    }
                    .home-link:hover {
                        background-color: #4338ca;
                    }
                    .home-link:focus {
                        outline: 2px solid #4f46e5;
                        outline-offset: 2px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="message">
                    Email Verified Successfully!
                    </div>
                    <a href="https://www.leeblock.ru" class="home-link">
                        Home
                    </a>
                </div>
            </body>
            </html>
            """
        return HTMLResponse(content=html_content)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
