from fastapi import APIRouter, Body, HTTPException, status, Response, Query
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID, uuid4
from pydantic import UUID4
from models.invitations import Invitation, InvitationUpdate, InvitationCreate, RsvpStatus
from clients.client import db, get_invitation_by_id, save_invitation
from utils.email_service import send_email, send_party_invitation_email
from utils.services import (
    get_latest_party_plan_by_id,
    calculate_latest_rsvp_count,
    update_rsvp_count_in_party_plan,
)
from datetime import datetime
from utils.authenticator import authenticator

router = APIRouter()


# server 201/ response 201, 422
@router.post(
    "/",
    response_description="Create a new invitation",
    status_code=status.HTTP_201_CREATED,
    response_model=Invitation,
)
def create_invitation(
    party_plan_id: UUID,
    # invitation: InvitationCreate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # dummy account
    account = {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "fullname": "Dummy Name",
        "email": "dummy.email@example.com",
    }

    required_keys = ["id", "fullname", "email"]

    account_info = {key: account.get(key) for key in required_keys}
    print("Debug: account_info:", account_info)

    if not all(account_info.get(key) for key in required_keys):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required account information is missing",
        )

    # find associated party plan
    associated_party_plan = db.party_plans.find_one({"id": str(party_plan_id)})
    print("Debug: associated_party_plan:", associated_party_plan)
    if not associated_party_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No party plan found with ID {party_plan_id}",
        )

    # id, timestamp, account info
    invitation_id = str(uuid4())
    invitation_data = {
        "id": invitation_id,
        "created": datetime.now(),
        "account": account_info,
        "party_plan_id": str(party_plan_id),
    }

    # add to db
    new_invitation = db.invitations.insert_one(invitation_data)
    print("Debug: new_invitation.acknowledged:", new_invitation.acknowledged)
    if not new_invitation.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add invitation to database.",
        )

    # Auto-Send the email
    email_sent = send_email(
        to_email=account_info['email'],
        subject="You're Invited!",
        content="You have been invited to a party! Click here to Accept/Decline."
    )

    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send invitation email."
        )

    # fetch the instance you just created
    created_invitation = db.invitations.find_one({"id": invitation_id})
    print("Debug: created_invitation:", created_invitation)
    if not created_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation with ID {invitation_data['id']} not found after insertion.",
        )

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


# server 200/ response 200, 422
@router.get(
    "/{id}",
    response_description="Get a single invitation by ID",
    response_model=Invitation,
)
def find_invitation(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (invitation := db.invitations.find_one({"id": id})) is not None:
        return invitation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invitation with ID {id} not found",
    )


# server 200/ response
@router.put(
    "/{id}",
    response_description="Update an invitation",
    response_model=Invitation,
)
def update_invitation(
    id: UUID,
    invitation: InvitationUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_invitation = db.invitations.find_one({"id": str(id)})

    if not existing_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation with ID {id} not found",
        )

    invitation_data = {
        k: v for k, v in invitation.dict().items() if v is not None
    }

    if invitation_data:
        db.invitations.update_one({"id": str(id)}, {"$set": invitation_data})

    return db.invitations.find_one({"id": str(id)})


@router.delete("/{id}", response_description="Delete an invitation")
def delete_invitation(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.invitations.delete_one({"id": id})
    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Invitation with ID {id}) successfully deleted.",
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
    location: str
):
    rsvp_link_accept = f'http://localhost:8000/rsvp/{invitation.id}?status=accept'
    rsvp_link_decline = f'http://localhost:8000/rsvp/{invitation.id}?status=decline'

    content = send_party_invitation_email(
        invitation.guest_name, party_name, date, location, rsvp_link_accept, rsvp_link_decline
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


@router.put("/rsvp/{invitation_id}/", response_model=Invitation)
async def update_rsvp_status(
    invitation_id: UUID,
    rsvp_status: RsvpStatus = Query(..., alias="status")
):
    print(f"Debug: Received invitation_id: {invitation_id}, rsvp_status: {rsvp_status}")
    invitation = db.invitations_collections.find_one({"id": invitation_id})
    print("Debug: Existing invitation:", invitation)
    if not invitation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invitation not found")

    # Update RSVP status in DB
    db.invitations_collections.update_one(
        {"id": invitation_id},
        {"$set": {"rsvp_status": rsvp_status}},
    )

    # Update RSVP count in the associated party plan
    party_plan_id = invitation.get("party_plan_id")
    party_plan = get_latest_party_plan_by_id(party_plan_id)
    new_rsvp_count = calculate_latest_rsvp_count(party_plan)
    update_rsvp_count_in_party_plan(party_plan_id, new_rsvp_count)

    # Send an email based on the RSVP status
    to_email = invitation.get("account").get("email")
    if rsvp_status == RsvpStatus.ACCEPTED:
        send_email(to_email, "RSVP Status Update", "You have accepted the invitation.")
    elif rsvp_status == RsvpStatus.DECLINED:
        send_email(to_email, "RSVP Status Update", "You have declined the invitation.")

    # Fetch the updated invitation
    updated_invitation = db.invitations_collections.find_one({"id": invitation_id})
    return updated_invitation
