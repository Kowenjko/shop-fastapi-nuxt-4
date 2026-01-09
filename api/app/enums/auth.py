from enum import StrEnum

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


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
