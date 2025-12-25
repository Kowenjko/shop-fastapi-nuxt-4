from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.services.user_service import UserService
from app.schemas.user import UserResponse, CreateUser

router = APIRouter(tags=["Users"])


@router.get(
    "/",
    response_model=list[UserResponse] | UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    username: str | None = None,
):
    user_service = UserService(session)
    if username:
        return await user_service.get_user_by_name(username)

    return await user_service.get_all_users()


@router.get("/{user_id}/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = UserService(session)
    return await service.get_user_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = UserService(session)
    return await service.create_user(user_data)
