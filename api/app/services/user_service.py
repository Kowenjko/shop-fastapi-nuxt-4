from typing import List
from app.repositories.user_repository import UserRepository
from app.schemas.user import CreateUser, UserResponse
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import hash_password


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_all_users(self) -> List[UserResponse]:
        users = await self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        self._not_user(user, str(user_id))

        return UserResponse.model_validate(user)

    async def get_user_by_name(self, username: str) -> UserResponse:
        user = await self.repository.get_by_username(username)
        self._not_user(user, username)
        return UserResponse.model_validate(user)

    async def create_user(self, user_data: CreateUser) -> UserResponse:
        username = await self.repository.get_by_username(user_data.username)
        if username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with username {user_data.username} already exists",
            )
        email = await self.repository.get_by_email(user_data.email)
        if email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user_data.email} already exists",
            )
        if len(user_data.password.encode("utf-8")) > 72:
            raise HTTPException(
                400,
                "Password is too long",
            )
        hashed_password = hash_password(user_data.password)

        user = await self.repository.create(
            {
                "username": user_data.username,
                "password_hash": hashed_password,
                "email": user_data.email,
                "role": "user",
            }
        )
        if not user:
            return None
        return UserResponse.model_validate(user)

    def _not_user(self, user, text: str):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {text} not found",
            )
