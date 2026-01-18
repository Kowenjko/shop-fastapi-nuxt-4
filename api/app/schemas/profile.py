from pydantic import BaseModel, Field, ConfigDict
from .user import UserResponse
from .city import CityResponse


class ProfileBase(BaseModel):
    first_name: str | None = Field(None, max_length=40, description="First name")
    last_name: str | None = Field(None, max_length=40, description="Last name")
    phone: str | None = Field(None, max_length=40, description="Phone number")
    city_id: str | None = Field(None, max_length=100, description="City id by user")
    age: int | None = Field(None, ge=0, description="Age")


class ProfileCreate(ProfileBase):
    user_id: int = Field(..., description="User ID")


class ProfileUpdate(ProfileBase):
    pass


class ProfilePostResponse(ProfileBase):

    id: int = Field(..., description="Unique profile ID")
    model_config = ConfigDict(from_attributes=True)


class ProfileResponse(ProfilePostResponse):

    user: UserResponse = Field(..., description="Associated user details")
    city: CityResponse | None = None

    model_config = ConfigDict(from_attributes=True)
