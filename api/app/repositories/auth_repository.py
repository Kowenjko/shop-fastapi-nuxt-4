from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import RefreshToken
from app.schemas.auth import CreateRefreshToken


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_refresh_token(self, refresh: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token == refresh)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, token_data: CreateRefreshToken) -> RefreshToken:
        refresh_token = RefreshToken(**token_data.model_dump())
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        return refresh_token

    async def delete(self, token: str):
        stmt = delete(RefreshToken).where(RefreshToken.token == token)
        await self.session.execute(stmt)
        await self.session.commit()

    async def delete_all_for_user(self, user_id: int):
        stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
