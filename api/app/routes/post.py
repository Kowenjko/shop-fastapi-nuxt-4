from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, Query, Request, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_validation import get_current_user_id
from app.core.db_helper import db_helper
from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostMetaResponse


router = APIRouter(tags=["Posts"])


# --- GET ---
@router.get("/all", response_model=List[PostResponse])
async def get_posts(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user_ids: Optional[List[int]] = Query(None),
):
    service = PostService(session)
    return await service.get_all_posts(limit=limit, offset=offset, user_ids=user_ids)


@router.get(
    "/",
    response_model=PostMetaResponse,
    status_code=status.HTTP_200_OK,
)
async def get_posts_paginated(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = PostService(session)
    return await service.get_posts_paginated(
        base_url=str(
            request.url.remove_query_params("page").remove_query_params("per_page")
        ),
        page=page,
        per_page=per_page,
    )


@router.get(
    "/user/",
    response_model=List[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_posts_by_user(
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    user_id: int = Depends(get_current_user_id),
):
    service = PostService(session)
    return await service.get_post_by_user_id(user_id)


@router.get("/{post_id}/", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(
    post_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
):
    service = PostService(session)
    return await service.get_post(post_id)


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
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    service = PostService(session)
    return await service.update_post(post_id, post_data, user_id)


# --- DELETE ---
@router.delete("/{post_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.scoped_session_dependency)],
    user_id: int = Depends(get_current_user_id),
):
    service = PostService(session)
    await service.delete_post(post_id, user_id)
