from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db_helper import db_helper
from app.core.oauth import oauth

from app.schemas.user import CreateUser, UserResponse
from app.services.user_service import UserService
from app.services.dependencies import get_current_user_id
from app.services.auth_service import AuthService

router = APIRouter(tags=["Auth"])

#    "username": "string7",
#    "email": "user7@example.com",
#    "password": "stringst7",

#


@router.get("/github/login/")
async def github_login(request: Request):
    return await oauth.github.authorize_redirect(
        request,
        redirect_uri="https://api.shop.local/auth/github/callback",
    )


@router.get("/github/callback")
async def github_callback(request: Request):
    print("Session data:", request.session)
    print("GET state:", request.query_params.get("state"))
    token = await oauth.github.authorize_access_token(request)
    user_data = await oauth.github.get("user", token=token)
    user_data = user_data.json()

    email_data = await oauth.github.get("user/emails", token=token)
    email = next(
        (e["email"] for e in email_data.json() if e["primary"]),
        None,
    )

    return email


@router.post("/login/")
async def login(
    response: Response,
    user_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = AuthService(session)
    access, refresh = await service.login(response, user_data)

    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


@router.post("/refresh/")
async def refresh(
    response: Response,
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = AuthService(session)

    access, new_refresh = await service.refresh(request)

    response.set_cookie(
        "refresh_token",
        new_refresh,
        httponly=True,
        secure=True,
        samesite="strict",
    )

    return {
        "access_token": access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }


@router.post(
    "/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: CreateUser,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = UserService(session)
    return await service.create_user(user_data)


@router.post("/logout/", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    response: Response,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = AuthService(session)
    await service.logout(user_id)

    response.delete_cookie("refresh_token")
