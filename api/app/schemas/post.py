from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .user import UserResponse
from .profile import ProfilePostResponse


class PostBase(BaseModel):
    title: str | None = Field(None, max_length=100, description="Title")
    content: Optional[str]


class PostCreate(PostBase):
    user_id: int = Field(..., description="User ID")


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique profile ID")
    user_id: int = Field(..., description="User ID")

    user: UserResponse = Field(..., description="Associated user details")
    profile: ProfilePostResponse = Field(..., description="Associated profile details")
