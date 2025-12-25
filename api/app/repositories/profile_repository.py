from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import Profile
from app.schemas.profile import ProfileCreate


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Profile]:
        stmt = select(Profile).order_by(Profile.id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, profile_id: int) -> Optional[Profile]:
        stmt = select(Profile).filter(Profile.id == profile_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[Profile]:
        stmt = select(Profile).filter(Profile.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, profile_data: ProfileCreate) -> Profile:
        db_profile = Profile(**profile_data.model_dump())
        self.session.add(db_profile)
        await self.session.commit()
        await self.session.refresh(db_profile)
        return db_profile
