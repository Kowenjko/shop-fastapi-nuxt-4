from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository

from app.models import User, Profile


async def profile_by_id(
    user_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Profile:
    repository = ProfileRepository(session)
    profile = await repository.get_by_user_id(user_id)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Profile for user id {user_id} not found",
        )
    return profile
