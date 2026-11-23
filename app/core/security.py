from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
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