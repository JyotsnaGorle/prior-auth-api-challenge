"""Database tables. First pass: only the core of the domain.

TODO (next sessions): members, practices, providers, reviewers, coverage,
patient_practice_links, reviewer_patient_links (conflict of interest), seed data.
"""
from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class RequestStatus(StrEnum):
    SUBMITTED = "submitted"    # in the queue
    IN_REVIEW = "in_review"    # claimed by a reviewer
    DECIDED = "decided"        # final; appeals are out of scope


class PriorAuthRequest(Base):
    __tablename__ = "prior_auth_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int]
    practice_id: Mapped[int]
    submitted_by_user_id: Mapped[int]
    diagnosis_code: Mapped[str] = mapped_column(String(10))  # ICD-10
    date_of_service: Mapped[date]
    clinical_note: Mapped[str | None] = mapped_column(Text)   # internal: never shown to members
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.SUBMITTED)
    assigned_reviewer_id: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    procedures: Mapped[list["RequestProcedure"]] = relationship(back_populates="request")


class RequestProcedure(Base):
    __tablename__ = "request_procedures"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("prior_auth_requests.id"))
    code: Mapped[str] = mapped_column(String(10))  # CPT or HCPCS
    units: Mapped[int]
    decision: Mapped[str | None]                   # "approved" / "denied"
    denial_reason: Mapped[str | None] = mapped_column(Text)  # internal

    request: Mapped[PriorAuthRequest] = relationship(back_populates="procedures")


class AuditEvent(Base):
    """Append-only record of who did what, when. Never updated or deleted."""

    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int | None]   # null for rejected submissions (support desk lookups)
    actor_user_id: Mapped[int]
    actor_role: Mapped[str]
    action: Mapped[str]              # e.g. "submitted", "claimed", "decided", "submission_rejected"
    details: Mapped[str | None] = mapped_column(Text)
    occurred_at: Mapped[datetime] = mapped_column(server_default=func.now())
