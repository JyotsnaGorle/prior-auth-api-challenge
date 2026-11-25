"""Endpoints for members (patients)."""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import Principal, Role, require_role

router = APIRouter(prefix="/member", tags=["member"])
member_only = require_role(Role.MEMBER)


@router.get("/requests")
def list_my_requests(principal: Principal = Depends(member_only)):
    # TODO: use a member-specific response schema that has NO clinical note
    # or denial reason fields, so they can't leak by accident.
    raise HTTPException(501, "Not implemented yet")
