import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.authenticator import authenticator
from models.invitations import get_invitation_by_id, update_invitation_rsvp
from routers import (
    party_plans,
    locations,
    invitations,
    accounts,
    notes,
    emails,
)

app = FastAPI()


app.include_router(
    party_plans.router, tags=["party plans"], prefix="/party_plans"
)
app.include_router(locations.router, tags=["locations"], prefix="/locations")
app.include_router(
    invitations.router, tags=["invitations"], prefix="/invitations"
)
app.include_router(locations.router, tags=["send-invitation"], prefix="/locations")
app.include_router(notes.router, tags=["notes"], prefix="/notes")
app.include_router(emails.router, tags=["emails"], prefix="/emails")

app.include_router(authenticator.router)
app.include_router(accounts.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/rsvp/{invitation_id}")
async def rsvp_invitation(invitation_id: str, status: str):
    invitation = get_invitation_by_id(invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")

    if status not in ['accept', 'decline']:
        raise HTTPException(status_code=400, detail="Invalid status")

    update_invitation_rsvp(invitation_id, status)
    return {"message": f"RSVP {status} successfully"}
