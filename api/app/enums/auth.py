from enum import StrEnum
from app.core.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class Providers(StrEnum):
    GITHUB = "github"
    GOOGLE = "google"


PROVIDER_CONFIG = {
    "github": settings.oauth.github,
    "google": settings.oauth.google,
}


class Permission(StrEnum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


ROLE_PERMISSIONS = {
    "user": [Permission.READ],
    "admin": [
        Permission.READ,
        Permission.WRITE,
        Permission.DELETE,
    ],
}
