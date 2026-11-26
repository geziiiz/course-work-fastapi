from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
ph = PasswordHasher()
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timedelta, timezone
from jose import jwt
def hash_password(password: str) -> str:
    """Хеширование пароля."""
    return ph.hash(password)
def verify_password(plain: str, hashed: str) -> bool:
    """Проверка пароля против хеша."""
    try:
        ph.verify(hashed, plain)
        return True
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def _create_token(data: dict[str, any], expires_delta: timedelta, token_type: str) -> str:
    """Создание токена """
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    to_encode.update({
        "exp": now + expires_delta, # Время истечения
        "iat": now, # Время выпуска (Issued At)
        "type": token_type,
        })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(data: dict) -> str:
    """Создание access-токена"""
    return _create_token(
        data,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), "access")

def create_refresh_token(data: dict) -> str:
    """Создание refresh-токена"""
    return _create_token(
        data,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), "refresh")