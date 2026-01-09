from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(64)]
    role: str = "user"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique category identifier")
    username: str
    email: EmailStr
    active: bool
    role: str


class UserAuth(UserResponse):
    pass
