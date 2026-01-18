from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_validation import get_current_user_id


from app.core.db_helper import db_helper

from app.repositories.profile_repository import ProfileRepository

from app.models import Profile


def _not_user(data, detail: str):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


async def profile_by_user_id(
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Profile:
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    repository = ProfileRepository(session)
    profile = await repository.get_by_user_id(user_id)

    _not_user(profile, f"Profile for user id {user_id} not found")
    return profile
