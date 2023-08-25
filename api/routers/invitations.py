from fastapi import APIRouter, Body, HTTPException, status, Response, Depends

from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID, uuid4
from utils.authenticator import authenticator
from models.invitations import Invitation, InvitationUpdate, InvitationCreate
from clients.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new invitation",
    status_code=status.HTTP_201_CREATED,
    response_model=Invitation,
)
def create_invitation(
    party_plan_id: UUID,
    invitation: InvitationCreate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # find associated party plan
    associated_party_plan = db.party_plans.find_one({"id": str(party_plan_id)})
    if not associated_party_plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No party plan found with ID {party_plan_id}",
        )
    # check that there's no id
    if "id" in invitation.dict():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request payload should not include 'id'. ID will be auto-generated.",
        )

    invitation_data = jsonable_encoder(invitation)

    # id generation
    invitation_id = str(uuid4())
    invitation_data["id"] = invitation_id
    invitation_data["party_plan_id"] = str(party_plan_id)

    # add to db
    new_invitation = db.invitations.insert_one(invitation_data)
    if not new_invitation.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add invitation to database.",
        )

    # fetch the instance you just created
    created_invitation = db.invitations.find_one({"id": invitation_data["id"]})
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
