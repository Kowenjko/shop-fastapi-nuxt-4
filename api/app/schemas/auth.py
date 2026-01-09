from pydantic import BaseModel


class CreateRefreshToken(BaseModel):
    user_id: int
    token: str
