from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models import Post, User
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, post_data: PostCreate) -> Post:
        post = Post(**post_data.model_dump())
        self.session.add(post)
        await self.session.commit()

        stmt = (
            select(Post)
            .where(Post.id == post.id)
            .options(selectinload(Post.user).selectinload(User.profile))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(self) -> List[Post]:
        stmt = (
            select(Post)
            .options(selectinload(Post.user).selectinload(User.profile))
            .order_by(Post.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_post_by_id(self, post_id: int) -> Post | None:
        stmt = (
            select(Post)
            .where(Post.id == post_id)
            .options(selectinload(Post.user).selectinload(User.profile))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[Post]:
        stmt = (
            select(Post)
            .where(Post.user_id == user_id)
            .options(selectinload(Post.user).selectinload(User.profile))
            .order_by(Post.id)
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, post: Post, post_data: PostUpdate) -> Post:
        for key, value in post_data.model_dump(exclude_unset=True).items():
            setattr(post, key, value)

        await self.session.commit()

        stmt = (
            select(Post)
            .where(Post.id == post.id)
            .options(selectinload(Post.user).selectinload(User.profile))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def delete(self, post: Post):
        await self.session.delete(post)
        await self.session.commit()
