from pydantic import BaseModel, Field, ConfigDict


class OrderBase(BaseModel):
    user_id: int = Field(..., description="User ID")
    total_amount: float = Field(
        ..., gt=0, description="Total order amount (must be greater than 0)"
    )
