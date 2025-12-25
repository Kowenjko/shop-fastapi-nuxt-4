from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.repositories.profile_repository import ProfileRepository


class Dependencies:

    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)
