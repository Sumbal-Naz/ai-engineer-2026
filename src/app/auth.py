from pwdlib import PasswordHash

from datetime import datetime, timedelta, timezone

import jwt

from src.app.config import settings

# Password hashing utility.
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Hash a plain-text password before storing it.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    Verify a plain-text password against its stored hash.
    """
    return password_hash.verify(
        plain_password,
        hashed_password
    )

def create_access_token(
    user_id: int,
    username: str
) -> str:
    """
    Create a signed JWT access token for an authenticated user.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )