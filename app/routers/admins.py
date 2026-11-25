"""Endpoints for operations admins."""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import Principal, Role, require_role

router = APIRouter(prefix="/admin", tags=["admin"])
admin_only = require_role(Role.ADMIN)


@router.get("/requests")
def list_all_requests(principal: Principal = Depends(admin_only)):
    raise HTTPException(501, "Not implemented yet")


@router.post("/requests/{request_id}/reassign")
def reassign(request_id: int, principal: Principal = Depends(admin_only)):
    raise HTTPException(501, "Not implemented yet")


@router.get("/requests/{request_id}/audit")
def audit_trail(request_id: int, principal: Principal = Depends(admin_only)):
    raise HTTPException(501, "Not implemented yet")
