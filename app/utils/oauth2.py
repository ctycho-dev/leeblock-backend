from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import SignatureExpired, BadSignature
from app.schemas.users import TokenData
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SALT = "email-verification"
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_verification_token(email: str) -> str:
    """
    Generate a secure token for email verification.

    Args:
        email (str): The email address to verify.

    Returns:
        str: The generated token.
    """
    return serializer.dumps(email, salt=SALT)


def decode_email_token(token: str):
    try:
        email = serializer.loads(token, salt=SALT, max_age=86400)
    except (SignatureExpired, BadSignature) as exc:
        raise ValueError("Invalid or expired token") from exc

    return email


def create_access_token(data: dict):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('user_id')

        if user_id is None:
            raise credentials_exception

        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    
    return token_data


def hash_pwd(password: str) -> str:
    """
    Generate a hash for a given password.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)
