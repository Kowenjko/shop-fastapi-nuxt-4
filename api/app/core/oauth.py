from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

oauth = OAuth()

oauth.register(
    name=settings.oauth.github.name,
    client_id=settings.oauth.github.client_id,
    client_secret=settings.oauth.github.client_secret,
    access_token_url=settings.oauth.github.access_token_url,
    authorize_url=settings.oauth.github.authorize_url,
    api_base_url=settings.oauth.github.api_base_url,
    client_kwargs=settings.oauth.github.client_kwargs,
)

oauth.register(
    name=settings.oauth.google.name,
    client_id=settings.oauth.google.client_id,
    client_secret=settings.oauth.google.client_secret,
    server_metadata_url=settings.oauth.google.server_metadata_url,
    client_kwargs=settings.oauth.google.client_kwargs,
)
