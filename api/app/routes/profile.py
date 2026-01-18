from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.services.profile_service import ProfileService
from app.schemas.profile import ProfileCreate, ProfileResponse, ProfileUpdate

from app.models import Profile
from app.services.dependencies import profile_by_user_id

router = APIRouter(tags=["Profile"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_profile(
    profile: Profile = Depends(profile_by_user_id),
):
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )
    return profile


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: ProfileCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = ProfileService(session)
    return await service.create_profile(profile_data)


@router.put("/", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def update_profile(
    profile_data: ProfileUpdate,
    profile: Profile = Depends(profile_by_user_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = ProfileService(session)
    return await service.update_profile(profile, profile_data)
