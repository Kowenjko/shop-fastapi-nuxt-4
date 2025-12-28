from typing import List
from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.schemas.user import UserResponse
from app.schemas.profile import ProfileResponse
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Post


class PostService:
    def __init__(self, session: AsyncSession):
        self.repository = PostRepository(session)

    async def get_all_posts(self) -> List[PostResponse]:
        posts = await self.repository.get_all()
        return [self._to_post_response(post) for post in posts]

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
