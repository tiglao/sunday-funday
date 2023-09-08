from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from clients.client import db

from clients.client import db
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from models.invitations import Invitation, InvitationPayload, InvitationUpdate
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
    invitation_payload: InvitationPayload = None,
):
    print("Debug: Received invitation_payload:", invitation_payload)
    account = {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "fullname": invitation_payload.fullName
        if invitation_payload
        else "Example Name",
        "email": invitation_payload.email
        if invitation_payload
        else "example.email@example.com",
    }
    print("Debug: Using dummy account:", account)
    required_keys = ["id", "fullname", "email"]

    account_info = {key: account.get(key) for key in required_keys}
    print("Debug: account_info:", account_info)

    if not all(account_info.get(key) for key in required_keys):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required account information is missing",
        )

    associated_party_plan = db.party_plans.find_one({"id": str(party_plan_id)})
    if not associated_party_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No party plan found with ID {party_plan_id}",
        )

    invitation_id = str(uuid4())
    invitation_data = {
        "id": invitation_id,
        "created": datetime.now(),
        "account": account_info,
        "party_plan_id": str(party_plan_id),
    }

    new_invitation = db.invitations.insert_one(invitation_data)
    if not new_invitation.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add invitation to database.",
        )

    created_invitation = db.invitations.find_one({"id": invitation_id})
    if not created_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation with ID {invitation_data['id']} not found after insertion.",
        )
    print("Debug: Created Invitation:", created_invitation)
    return created_invitation


@router.get(
    "/",
    response_description="List all invitations",
    response_model=List[Invitation],
)
def list_invitations():
    invitations = list(db.invitations.find(limit=100))
    return invitations


@router.get(
    "/{id}",
    response_description="Get a single invitation by ID",
    response_model=Invitation,
)
def find_invitation(
    id: str,
):
    if (invitation := db.invitations.find_one({"id": id})) is not None:
        return invitation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invitation with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update an invitation",
    response_model=Invitation,
)
def update_invitation(
    id: UUID,
    invitation: InvitationUpdate = Body(...),
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
