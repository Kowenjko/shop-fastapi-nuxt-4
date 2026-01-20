from typing import List
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Profile


class ProfileService:
    def __init__(self, session: AsyncSession):
        self.repository = ProfileRepository(session)

    async def get_profile_by_user_id(self, user_id: int) -> ProfileResponse:
        profile = await self.repository.get_by_user_id(user_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile for user id {user_id} not found",
            )
        return ProfileResponse.model_validate(profile)

    async def create_profile(self, profile_data: ProfileCreate) -> ProfileResponse:
        result = await self.repository.get_by_user_id(profile_data.user_id)
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Profile for user id {profile_data.user_id} already exists",
            )
        profile = await self.repository.create(profile_data)
        return ProfileResponse.model_validate(profile)

    async def update_profile(
        self, profile: Profile, profile_data: ProfileUpdate
    ) -> ProfileResponse:

        updated_profile = await self.repository.update(profile, profile_data)
        return ProfileResponse.model_validate(updated_profile)
