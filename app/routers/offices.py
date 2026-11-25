"""Endpoints for provider offices."""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import Principal, Role, require_role

router = APIRouter(prefix="/office", tags=["office"])
office_only = require_role(Role.OFFICE)


@router.post("/requests", status_code=201)
def submit_request(principal: Principal = Depends(office_only)):
    # TODO: validate (patient linked to practice, coverage active on DOS,
    # DOS not in the past and <= 1 year out, units <= 30), return every error
    # with the field to fix, write audit event (also on rejection).
    raise HTTPException(501, "Not implemented yet")


@router.get("/requests")
def list_my_requests(principal: Principal = Depends(office_only)):
    raise HTTPException(501, "Not implemented yet")
