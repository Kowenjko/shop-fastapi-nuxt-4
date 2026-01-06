from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_and_update_password(
    plain_password: str,
    hashed_password: str,
) -> str | None:
    try:
        verified, new_hash = pwd_context.verify_and_update(
            plain_password,
            hashed_password,
        )
        if not verified:
            return None
        return new_hash or hashed_password
    except:
        return None


def create_access_token(
    user_id: int,
    role: str,
    permissions: list[str],
) -> str:
    payload = {
        "sub": str(user_id),
        "role": role,
        "permissions": permissions,
        "type": "access",
        "exp": datetime.utcnow()
        + timedelta(minutes=settings.auth_jwt.access_token_expire_minutes),
    }
    return jwt.encode(
        payload,
        settings.auth_jwt.private_jwt_key.read_text(),
        algorithm=settings.auth_jwt.algorithm,
    )


def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow()
        + timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    }
    return jwt.encode(
        payload,
        settings.auth_jwt.private_jwt_key.read_text(),
        algorithm=settings.auth_jwt.algorithm,
    )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
