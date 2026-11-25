"""Endpoints for reviewers (nurses and physicians)."""
from fastapi import APIRouter, Depends, HTTPException

from app.auth import Principal, Role, require_role

router = APIRouter(prefix="/reviewer", tags=["reviewer"])
reviewer_only = require_role(Role.REVIEWER)


@router.get("/queue")
def view_queue(principal: Principal = Depends(reviewer_only)):
    # TODO: exclude requests for patients this reviewer treats.
    raise HTTPException(501, "Not implemented yet")


@router.post("/requests/{request_id}/claim")
def claim_request(request_id: int, principal: Principal = Depends(reviewer_only)):
    # TODO: atomic claim (SELECT ... FOR UPDATE), conflict-of-interest check, audit.
    raise HTTPException(501, "Not implemented yet")


@router.post("/requests/{request_id}/decision")
def submit_decision(request_id: int, principal: Principal = Depends(reviewer_only)):
    # TODO: a decision for every procedure, reason required for denials,
    # only the assigned reviewer, final once made, audit in the same transaction.
    raise HTTPException(501, "Not implemented yet")
