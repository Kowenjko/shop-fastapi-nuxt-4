from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt

from app.core.db_helper import db_helper

from app.repositories.profile_repository import ProfileRepository

from app.models import Profile


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_payload(
    token: str = Depends(oauth2_scheme),
):
    payload = jwt.decode(
        token,
        settings.auth_jwt.private_jwt_key.read_text(),
        algorithms=[settings.auth_jwt.algorithm],
    )
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return payload


async def get_current_user_id(
    payload: dict = Depends(get_payload),
) -> int:
    return int(payload["sub"])


def require_permissions(*perms: str):

    async def checker(payload: dict = Depends(db_helper.session_getter)):
        if not all(p in payload["permissions"] for p in perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )

    return checker


def _not_user(data, detail: str):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


async def profile_by_user_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Profile:
    repository = ProfileRepository(session)
    profile = await repository.get_by_user_id(user_id)

    _not_user(profile, f"Profile for user id {user_id} not found")
    return profile
