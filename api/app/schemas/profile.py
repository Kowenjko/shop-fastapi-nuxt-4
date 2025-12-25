from pydantic import BaseModel, Field, ConfigDict


class ProfileBase(BaseModel):
    first_name: str | None = Field(None, max_length=40, description="First name")
    last_name: str | None = Field(None, max_length=40, description="Last name")
    phone: str | None = Field(None, max_length=40, description="Phone number")
    address: str | None = Field(None, max_length=255, description="Address")
    age: int | None = Field(None, ge=0, description="Age")


class ProfileCreate(ProfileBase):
    user_id: int = Field(..., description="User ID")


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique profile ID")
    user_id: int = Field(..., description="User ID")
