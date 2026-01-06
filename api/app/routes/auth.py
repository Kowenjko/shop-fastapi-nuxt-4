from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db_helper import db_helper

from app.schemas.user import CreateUser, UserResponse
from app.services.user_service import UserService
from app.services.dependencies import get_current_user_id
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])


@router.post("/login")
async def login(
    response: Response,
    user_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = AuthService(session)
    access = await service.login(response, user_data)

    return {"access_token": access, "token_type": "bearer"}


@router.post("/refresh")
async def refresh(
    request: Request, session: AsyncSession = Depends(db_helper.session_getter)
):
    service = AuthService(session)
    access = await service.refresh(request)

    return {"access_token": access, "token_type": "bearer"}


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: CreateUser,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = UserService(session)
    return await service.create_user(user_data)


@router.post("/logout", status_code=204)
async def logout(
    response: Response,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = UserService(session)
    await service(user_id)

    response.delete_cookie("refresh_token")
