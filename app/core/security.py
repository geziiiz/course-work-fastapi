from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.models.user import User
from app.database.session import get_session
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

ph = PasswordHasher()
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
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), 
        "access"
        )

def create_refresh_token(data: dict) -> str:
    """Создание refresh-токена"""
    return _create_token(
        data,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), 
        "refresh"
        )

def decode_token(token: str) -> dict | None:
    """Декодирование токена"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_user_from_token(token: str, session: Session) -> User | None:
    """Поиск пользователя по токену"""
    payload = decode_token(token)
    if payload is None:
        return None
    email = payload.get("sub")
    if email is None:
        return None
    return session.exec(
        select(User).where(User.email == email)
    ).first()


# ─── 5. Зависимость FastAPI (мост) ───────────────────────

bearer_scheme = HTTPBearer()
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_session)) -> User | None:
    """Поиск пользователя (авторизация с помощью HTTPBearer)"""
    token = credentials.credentials
    return get_user_from_token(token, session)