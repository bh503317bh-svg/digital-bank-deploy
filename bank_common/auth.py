from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DEFAULT_SECRET = "wecode-bank-demo-secret-change-me"
DEFAULT_ALG = "HS256"
DEFAULT_EXPIRE_MINUTES = 60 * 24


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(
    subject: str,
    *,
    role: str,
    user_id: int,
    secret: str = DEFAULT_SECRET,
    expire_minutes: int = DEFAULT_EXPIRE_MINUTES,
    extra: Optional[dict[str, Any]] = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "uid": user_id,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=expire_minutes),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, secret, algorithm=DEFAULT_ALG)


def decode_token(token: str, secret: str = DEFAULT_SECRET) -> dict[str, Any]:
    return jwt.decode(token, secret, algorithms=[DEFAULT_ALG])
