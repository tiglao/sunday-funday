from fastapi import APIRouter, Body, HTTPException, status, Response
from typing import List
from uuid import UUID, uuid4
from models.invitations import Invitation, InvitationUpdate, InvitationCreate
from clients.client import db
from utils.email_service import send_email
from datetime import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.invitations import Invitation, InvitationPayload, InvitationUpdate
from utils.authenticator import authenticator
import logging


router = APIRouter()

logging.basicConfig(level=logging.INFO)


# server 201/ response 201, 422
@router.post(
    "/",
    response_description="Create a new invitation",
    status_code=status.HTTP_201_CREATED,
    response_model=Invitation,
)
def create_invitation(
    party_plan_id: UUID,
    invitation_payload: InvitationPayload = None,
    # invitation: InvitationCreate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    print("Debug: Received invitation_payload:", invitation_payload)
    account = {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "fullname": "Dummy Name",
        "email": "jc.marti.2809@gmail.com",
    }
    try:
        # find associated party plan
        associated_party_plan = db.party_plans.find_one({"id": str(party_plan_id)})
        if not associated_party_plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No party plan found with ID {party_plan_id}",
            )

        # id, timestamp, account info
        invitation_id = str(uuid4())
        invitation_data = {
            "id": invitation_id,
            "created": datetime.now(),
            "account": account,  # Replace with your real account data
            "party_plan_id": str(party_plan_id),
        }

        # add to db
        new_invitation = db.invitations.insert_one(invitation_data)
        if not new_invitation.acknowledged:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add invitation to database.",
            )

        party_name = associated_party_plan.get("name", "a party")
        email_content = f"You have been invited to {party_name}!"
        logging.info("About to send email...")

        # Auto-Send the email
        email_sent = send_email(
            to_email=account['email'],
            subject="You're Invited!",
            content=email_content
        )
        if not email_sent:
            logging.error("Failed to send invitation email.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send invitation email."
            )
        # Fetch the created invitation from the database
        created_invitation = db.invitations.find_one({"id": invitation_id})
        if not created_invitation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Invitation with ID {invitation_data['id']} not found after insertion.",
            )

        return created_invitation

    except Exception as e:
        logging.error(f"General Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


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
