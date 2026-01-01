from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import Profile
from app.schemas.profile import ProfileCreate


class ProfileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, profile_data: ProfileCreate) -> Profile:
        db_profile = Profile(**profile_data.model_dump())
        self.session.add(db_profile)
        await self.session.commit()
        await self.session.refresh(db_profile)
        return db_profile

    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        stmt = (
            select(Profile)
            .options(joinedload(Profile.user))
            .options(joinedload(Profile.city))
            .where(Profile.user_id == user_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, profile: Profile, profile_data: ProfileCreate) -> Profile:
        for key, value in profile_data.model_dump().items():
            setattr(profile, key, value)
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile
