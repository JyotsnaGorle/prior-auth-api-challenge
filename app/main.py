from fastapi import FastAPI

from app.routers import admins, members, offices, reviewers

app = FastAPI(
    title="Prior Authorization API",
    description="Submit, review and track prior authorization requests.",
)

# One router per user group: each group's roadmap can change independently,
# and new groups (auditors next) get their own router.
for r in (offices.router, reviewers.router, members.router, admins.router):
    app.include_router(r)


@app.get("/health")
def health():
    return {"status": "ok"}
