from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import CreateRefreshToken


from app.helpers.auth import create_access_token, create_refresh_token

from app.services.auth_validation import get_refresh_user
from fastapi.security import OAuth2PasswordRequestForm


class AuthService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session
        self.user_repository = UserRepository(session)
        self.auth_repository = AuthRepository(session)

    async def login(
        self, response: Response, user_data: OAuth2PasswordRequestForm
    ) -> str:

        user = await self.user_repository.get_by_username(user_data.username)
        return await self.issue_tokens(user, response)

    async def refresh(
        self,
        request: Request,
        response: Response,
    ) -> str:
        refresh = request.cookies.get("refresh_token")

        user = await get_refresh_user(self.session, refresh)
        return await self.issue_tokens(user, response)

    async def logout(self, user_id: int):
        await self.auth_repository.delete_all_for_user(user_id)

    async def issue_tokens(self, user: User, response: Response):
        access = create_access_token(user)
        refresh = create_refresh_token(user)

        await self.auth_repository.create(
            CreateRefreshToken(token=refresh, user_id=user.id)
        )

        response.set_cookie(
            "refresh_token",
            refresh,
            httponly=True,
            samesite="lax",
        )
        response.set_cookie(
            "access_token",
            access,
            httponly=True,
            samesite="lax",
        )

        return access, refresh
