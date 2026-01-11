from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidTokenError


from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_helper import db_helper

from app.utils import decode_jwt, validate_password
from app.schemas.user import UserResponse
from app.enums import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


def get_current_user_id(
    payload: dict = Depends(get_current_token_payload),
) -> int:
    return int(payload["sub"])


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserResponse:
    response = UserRepository(session)
    user = await response.get_by_id(user_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    async def dependency(
        payload: dict = Depends(get_current_token_payload),
        session: AsyncSession = Depends(db_helper.session_getter),
    ) -> User:
        validate_token_type(payload, token_type)
        user_id = int(payload["sub"])
        response = UserRepository(session)
        user = await response.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalid (user not found)",
            )
        return user

    return dependency


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


def validate_auth_user(user_data: OAuth2PasswordRequestForm, user: User | None) -> None:

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username",
        )

    if not validate_password(
        password=user_data.password,
        hashed_password=user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid password",
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )


async def get_refresh_user(session: AsyncSession, refresh: str) -> User:
    auth_repository = AuthRepository(session)

    if not refresh:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="refresh token missing",
        )

    try:
        payload = decode_jwt(token=refresh)
    except ExpiredSignatureError:
        raise HTTPException(401, "refresh token expired")
    except InvalidTokenError:
        raise HTTPException(401, "invalid refresh token")

    if payload.get("type") != REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token type invalid",
        )

    refresh_token = await auth_repository.get_refresh_token(refresh)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )

    await auth_repository.delete(refresh)

    user = await session.get(User, int(payload["sub"]))

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid (user not found)",
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user
