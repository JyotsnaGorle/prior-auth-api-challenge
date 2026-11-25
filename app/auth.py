"""Fake identity.

The real identity service issues a token holding a user ID and a role. Here the
token is just "<role>:<user_id>", e.g. `Authorization: Bearer office:42`.
Swapping in real JWT verification later should only touch this file.
"""
from dataclasses import dataclass
from enum import StrEnum

from fastapi import Depends, Header, HTTPException, status


class Role(StrEnum):
    MEMBER = "member"
    OFFICE = "office"
    REVIEWER = "reviewer"
    ADMIN = "admin"


@dataclass(frozen=True)
class Principal:
    user_id: int
    role: Role


def current_principal(authorization: str | None = Header(default=None)) -> Principal:
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing token")
    try:
        scheme, token = authorization.split(" ", 1)
        role, user_id = token.split(":", 1)
        if scheme.lower() != "bearer":
            raise ValueError
        return Principal(user_id=int(user_id), role=Role(role))
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


def require_role(role: Role):
    """Dependency factory: reject callers that don't have the given role."""

    def checker(principal: Principal = Depends(current_principal)) -> Principal:
        if principal.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Requires role '{role}'")
        return principal

    return checker
