from typing import Literal
from fastapi import HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.profile import ProfileCreate
from app.core.oauth import oauth
from app.enums import Providers, PROVIDER_CONFIG

from app.repositories.auth_repository import AuthRepository
from app.repositories.oauth_repository import OAuthRepository
from app.repositories.user_repository import UserRepository

from app.services.auth_service import AuthService
from app.services.profile_service import ProfileService


def get_client_config(provider: Providers):
    config = PROVIDER_CONFIG.get(provider)
    if not config:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    client = oauth.create_client(provider)
    if not client:
        raise HTTPException(status_code=400, detail="Unsupported provider")

    return config, client


class OAuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session)
        self.oauth_repository = OAuthRepository(session)
        self.auth_repository = AuthRepository(session)
        self.auth_service = AuthService(session)
        self.profile_service = ProfileService(session)

    async def oauth_login(
        self,
        provider: str,
        provider_id: str,
        email: str | None,
        username: str,
        response: Response,
    ):
        account = await self.oauth_repository.get_account(provider, provider_id)

        if account:
            user = account.user
        else:
            user = await self.user_repository.get_by_email(email) if email else None

            if not user:
                user = await self.user_repository.create(
                    {
                        "username": username,
                        "password_hash": None,
                        "email": email,
                        "role": "user",
                    }
                )

                profile_data = ProfileCreate(
                    first_name=user.username,
                    last_name=None,
                    phone=None,
                    age=None,
                    user_id=user.id,
                    city_id=None,
                )

                await self.profile_service.create_profile(profile_data)
            await self.oauth_repository.create(provider, provider_id, user.id)

        return await self.auth_service.issue_tokens(user, response)

    async def link_account(self, user_id: int, provider: str, provider_id: str):
        existing = await self.oauth_repository.get_account(provider, provider_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OAuth account already linked",
            )
        await self.oauth_repository.create(provider, provider_id, user_id)

    async def unlink_account(self, user_id: int, provider: str):
        await self.oauth_repository.unlink(user_id, provider)
