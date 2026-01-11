from fastapi import APIRouter, Depends, Response, Request

from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.config import settings
from app.enums import Providers

from app.services.oauth_service import OAuthService, get_client_config
from app.services.auth_validation import get_current_user_id

router = APIRouter(tags=["Provider"])


@router.get("/{provider}/login")
async def oauth_link(provider: Providers, request: Request):
    config, client = get_client_config(provider)

    return await client.authorize_redirect(
        request,
        redirect_uri=config.redirect_uri,
    )


@router.get("/{provider}/callback")
async def oauth_callback(
    provider: Providers,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(db_helper.session_getter),
):

    config, client = get_client_config(provider)
    token = await client.authorize_access_token(request)

    # --- provider specific data ---
    if provider == "github":
        profile = (await client.get("user", token=token)).json()
        emails = (await client.get("user/emails", token=token)).json()
        email = next((e["email"] for e in emails if e.get("primary")), None)
        provider_id = str(profile["id"])
        username = profile["login"]

    elif provider == "google":
        profile = await client.parse_id_token(request, token)
        provider_id = profile["sub"]
        email = profile.get("email")
        username = profile.get("name") or email.split("@")[0]

    service = OAuthService(session)

    access, refresh = await service.oauth_login(
        provider=provider,
        provider_id=provider_id,
        email=email,
        username=username,
        response=response,
    )

    redirect = RedirectResponse(
        url=settings.oauth.frontend_redirect,
        status_code=302,
    )

    redirect.set_cookie(
        "access_token",
        access,
        httponly=True,
        secure=True,
        samesite="none",
    )
    redirect.set_cookie(
        "refresh_token",
        refresh,
        httponly=True,
        secure=True,
        samesite="none",
    )

    return redirect


@router.post("/{provider}/link", status_code=201)
async def link_oauth_account(
    provider: Providers,
    provider_id: str,  # обычно приходит из OAuth callbacks
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = OAuthService(session)
    await service.link_account(
        user_id=user_id, provider=provider, provider_id=provider_id
    )
    return {"detail": f"{provider} account linked successfully"}


@router.delete("/{provider}/unlink", status_code=204)
async def unlink_oauth_account(
    provider: Providers,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = OAuthService(session)
    await service.unlink_account(user_id=user_id, provider=provider)
    return Response(status_code=204)
