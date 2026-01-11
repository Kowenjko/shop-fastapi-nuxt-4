from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import OAuthAccount


class OAuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_account(self, provider: str, provider_id: str) -> OAuthAccount | None:
        stmt = (
            select(OAuthAccount)
            .options(selectinload(OAuthAccount.user))
            .where(
                OAuthAccount.provider == provider,
                OAuthAccount.provider_account_id == provider_id,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, provider: str, provider_id: str, user_id: int):
        account = OAuthAccount(
            provider=provider,
            provider_account_id=provider_id,
            user_id=user_id,
        )
        self.session.add(account)
        await self.session.commit()
        await self.session.refresh(account)
        return account

    async def unlink(self, user_id: int, provider: str):
        stmt = select(OAuthAccount).where(
            OAuthAccount.user_id == user_id,
            OAuthAccount.provider == provider,
        )
        result = await self.session.execute(stmt)
        account = result.scalar_one_or_none()
        if account:
            await self.session.delete(account)
            await self.session.commit()

    async def delete(self, provider: str, provider_id: str):
        account = await self.get_account(provider, provider_id)
        if account:
            await self.session.delete(account)
            await self.session.commit()
