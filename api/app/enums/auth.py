from enum import StrEnum


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
