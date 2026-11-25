# Decisions and assumptions (work in progress)

## Architecture
- **FastAPI + SQLAlchemy 2 + PostgreSQL.** FastAPI generates OpenAPI docs at `/docs`, which partners can build from.
- **One router per user group** (`app/routers/`). Each group changes independently; auditors become a new router.
- **Fake auth:** `Authorization: Bearer <role>:<user_id>`. Only `app/auth.py` knows the token format.

## Ambiguities to resolve (draft calls, revisit)
| Requirement | Question | Draft decision |
|---|---|---|
| "Not in the past", "nationwide, Maine to Hawaii" | Whose "today"? | Compare date of service with today in the practice's time zone (store a tz per practice). |
| "More than 30 units is almost always a typo" | Reject or warn? | TBD: reject with a clear message, or require an explicit confirm flag. |
| "Reviewer must never review a patient they treat" | How do we know? | Seed a reviewer–patient treatment link; hide those requests from the queue and block claims. |
| "Decisions are final" | Partial approvals? | Allowed per procedure; the request is `decided` once every procedure has a decision. |
| "Admins see everything" vs. HIPAA minimum necessary | Do admins see clinical notes? | TBD. |
| "Submission didn't go through" | No request row exists | Log rejected submissions as audit events with the validation errors. |
| Audit "approved with no approver" | | Decision and audit event written in the same transaction; decision stores reviewer ID (NOT NULL). |
