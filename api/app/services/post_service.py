from math import ceil
from typing import List, Optional
from urllib.parse import urlencode
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostMetaResponse
from app.schemas.paginate import PaginateBase, PaginationLinks
from app.schemas.user import UserResponse
from app.schemas.profile import ProfileResponse
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post


class PostService:
    def __init__(self, session: AsyncSession):
        self.repository = PostRepository(session)

    async def get_all_posts(
        self, limit: int = 50, offset: int = 0, user_ids: Optional[List[int]] = None
    ) -> List[PostResponse]:
        if user_ids:
            posts = await self.repository.get_by_user_ids(user_ids, limit, offset)
        else:
            posts = await self.repository.get_all(limit, offset)
        return [self._to_post_response(post) for post in posts]

    async def get_posts_paginated(
        self,
        base_url: str,
        page: int = 1,
        per_page: int = 10,
    ) -> PostMetaResponse:

        # COUNT делаем только на первой странице
        with_total = page == 1

        posts, has_prev, has_next, total_items = (
            await self.repository.get_all_paginated(
                page=page,
                per_page=per_page,
                with_total=with_total,
            )
        )

        total_pages = ceil(total_items / per_page) if total_items is not None else None

        def build_link(page_number: int) -> str:
            query = urlencode({"page": page_number, "per_page": per_page})
            return f"{base_url}?{query}"

        return PostMetaResponse(
            items=[self._to_post_response(p) for p in posts],
            meta=PaginateBase(
                page=page,
                per_page=per_page,
                total_items=total_items,
                total_pages=total_pages,
                previous_page=page - 1 if has_prev else None,
                next_page=page + 1 if has_next else None,
                links={
                    "current": build_link(page),
                    "next": build_link(page + 1) if has_next else None,
                    "prev": build_link(page - 1) if has_prev else None,
                },
            ),
        )

    async def get_post(self, post_id: int) -> PostResponse:
        post = await self.repository.get_post_by_id(post_id)

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        return self._to_post_response(post)

    async def get_post_by_user_id(
        self,
        user_id: int,
    ) -> List[PostResponse]:

        posts = await self.repository.get_by_user_id(user_id)

        if not posts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post for user id {user_id} not found",
            )

        return [self._to_post_response(post) for post in posts]

    async def create_post(self, post_data: PostCreate) -> PostResponse:
        post = await self.repository.create(post_data)
        return self._to_post_response(post)

    async def update_post(
        self, post_id: int, post_data: PostUpdate, user_id: int
    ) -> PostResponse:
        post = await self.repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )
        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot delete someone else's post",
            )

        post = await self.repository.update(post, post_data)
        return self._to_post_response(post)

    async def delete_post(self, post_id: int, user_id: int):
        post = await self.repository.get_post_by_id(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        if post.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot delete someone else's post",
            )

        await self.repository.delete(post)

    def _to_post_response(self, post: Post) -> PostResponse:

        return PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            user_id=post.user_id,
            user=UserResponse.model_validate(post.user),
            profile=(
                ProfileResponse.model_validate(post.user.profile)
                if post.user.profile
                else None
            ),
        )
