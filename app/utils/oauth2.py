from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.schemas.users import TokenData
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """Access token."""
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


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
    "Hashing password"
    return pwd_context.hash(password)


def verify_pwd(plain_pwd: str, hashed_pwd: str):
    "Vetifying provided password"
    return pwd_context.verify(plain_pwd, hashed_pwd)