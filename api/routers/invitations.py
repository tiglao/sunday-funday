from fastapi import APIRouter, Body, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import uuid, UUID
from models.invitations import Invitation, InvitationUpdate
from clients.client import db
from utils.email_service import send_email, party_invitation_template
from clients.client import get_database

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new invitation",
    status_code=status.HTTP_201_CREATED,
    response_model=Invitation,
)
def create_invitation(
    plan: Invitation = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    plan = jsonable_encoder(plan)
    new_invitation = db.invitations.insert_one(plan)
    created_invitation = db.invitations.find_one(
        {"_id": new_invitation.inserted_id}
    )
    created_invitation["_id"] = str(created_invitation["_id"])
    return created_invitation


@router.get(
    "/",
    response_description="List all invitations",
    response_model=List[Invitation],
)
def list_invitations(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    invitations = list(db.invitations.find(limit=100))
    return invitations


@router.get(
    "/{id}",
    response_description="Get a single invitation by ID",
    response_model=Invitation,
)
def find_invitation(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (invitation := db.invitations.find_one({"_id": id})) is not None:
        return invitation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invitation with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update an invitation",
    response_model=InvitationUpdate,
)
def update_invitation(
    id: UUID,
    invitation: InvitationUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_invitation = db.invitations.find_one({"_id": str(id)})

    if not existing_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation with ID {id} not found",
        )

    invitation_data = {
        k: v for k, v in invitation.dict().items() if v is not None
    }

    if invitation_data:
        db.invitations.update_one({"_id": str(id)}, {"$set": invitation_data})

    return db.invitations.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete an invitation")
def delete_invitation(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.invitations.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Invitation with id {id}) successfully deleted.",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No invitation with ID {id} found. Deletion incomplete.",
    )


@router.post("/send-invitation/")
async def send_invitation(
    invitation: Invitation,
    party_name: str,
    date: str,
    location: str,
    rsvp_link: str,
):
    content = party_invitation_template(
        invitation.guest_name, party_name, date, location, rsvp_link
    )
    subject = f"You're Invited to {party_name}!"

    success = send_email(invitation.email, subject, content)

    if success:
        return {"status": "success", "message": "Invitation sent successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to send the invitation",
        )


@router.put("/rsvp/{invitation_id}/")
async def update_rsvp(invitation_id: str, status: bool):
    db = get_database()
    collection = db["invitations"]

    result = collection.update_one(
        {"_id": uuid.UUID(invitation_id)},
        {"$set": {"rsvpStatus": status}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Invitation not found")

    return {"status": "success", "message": "RSVP status updated successfully"}
