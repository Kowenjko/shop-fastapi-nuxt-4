from typing import Annotated, List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate, PostResponse


router = APIRouter(tags=["Posts"])


# --- GET ---
@router.get("/", response_model=List[PostResponse], status_code=status.HTTP_200_OK)
async def get_posts(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = PostService(session)
    return await service.get_all_posts()


@router.get("/{post_id}/", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(
    post_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = PostService(session)
    return await service.get_post(post_id)


@router.get(
    "/user/{user_id}/",
    response_model=List[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = PostService(session)
    return await service.get_post_by_user_id(user_id)


# --- POST ---
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = PostService(session)
    return await service.create_post(post_data)


# --- PUT ---
@router.put("/{post_id}/", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = PostService(session)
    return await service.update_post(post_id, post_data, user_id)


# --- DELETE ---
@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = PostService(session)
    await service.delete_post(post_id, user_id)
