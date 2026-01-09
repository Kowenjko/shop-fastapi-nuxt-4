from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository

from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import CreateRefreshToken


from app.helpers.auth import create_access_token, create_refresh_token

from app.services.auth_validation import validate_auth_user, get_refresh_user
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

        validate_auth_user(user_data=user_data, user=user)

        access = create_access_token(user)
        refresh = create_refresh_token(user)

        token_data = CreateRefreshToken(token=refresh, user_id=user.id)

        await self.auth_repository.create(token_data)

        response.set_cookie(
            "refresh_token",
            refresh,
            httponly=True,
            samesite="lax",
        )

        return access, refresh

    async def refresh(self, request: Request) -> str:
        refresh = request.cookies.get("refresh_token")

        user = await get_refresh_user(self.session, refresh)

        new_refresh = create_refresh_token(user)
        token_data = CreateRefreshToken(token=new_refresh, user_id=user.id)

        await self.auth_repository.create(token_data)

        access = create_access_token(user)

        return access, new_refresh

    async def logout(self, user_id: int):
        await self.auth_repository.delete_all_for_user(user_id)
