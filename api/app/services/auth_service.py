from app.enums.auth import ROLE_PERMISSIONS
from app.models import RefreshToken, User
from app.repositories.user_repository import UserRepository

from fastapi import HTTPException, Request, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth_security import (
    create_access_token,
    create_refresh_token,
    verify_and_update_password,
)
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from app.core.config import settings
from sqlalchemy import delete, select


class AuthService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.user_repository = UserRepository(session)

    async def login(
        self, response: Response, user_data: OAuth2PasswordRequestForm
    ) -> str:

        user = await self.user_repository.get_by_username(user_data.username)
        if not user or not user.active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        new_hash = verify_and_update_password(
            user_data.password,
            user.password,
        )
        if not new_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if new_hash != user.password:
            user.password = new_hash
            await self.session.commit()

        permissions = ROLE_PERMISSIONS[user.role]
        access = create_access_token(
            user.id,
            user.role,
            permissions,
        )
        refresh = create_refresh_token(user.id)

        self.session.add(RefreshToken(token=refresh, user_id=user.id))
        await self.session.commit()

        response.set_cookie(
            "refresh_token",
            refresh,
            httponly=True,
            samesite="lax",
        )

        return access

    async def refresh(self, request: Request) -> str:
        refresh = request.cookies.get("refresh_token")
        if not refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token invalid",
            )

        payload = jwt.decode(
            refresh,
            settings.auth_jwt.private_jwt_key.read_text(),
            algorithms=[settings.auth_jwt.algorithm],
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token type invalid",
            )

        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token == refresh)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="base invalid",
            )

        user = await self.session.get(User, int(payload["sub"]))
        permissions = ROLE_PERMISSIONS[user.role]

        access = create_access_token(
            user.id,
            user.role,
            permissions,
        )

        return access

    async def logout(self, user_id: int):
        await self.session.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        await self.session.commit()
