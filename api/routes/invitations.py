from fastapi import APIRouter, Body, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID

from queries.invitations import Invitation, InvitationUpdate
from queries.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new invitation",
    status_code=status.HTTP_201_CREATED,
    response_model=Invitation,
)
def create_invitation(plan: Invitation = Body(...)):
    plan = jsonable_encoder(plan)
    new_invitation = db.invitations.insert_one(plan)
    created_invitation = db.invitations.find_one(
        {"_id": new_invitation.inserted_id}
    )
    created_invitation["_id"] = str(created_invitation["_id"])
    return created_invitation


@router.get(
    "/",
    response_description="List all parties",
    response_model=List[Invitation],
)
def list_invitations():
    parties = list(db.invitations.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single invitation by id",
    response_model=Invitation,
)
def find_invitation(
    id: str,
):
    if (invitation := db.invitations.find_one({"_id": id})) is not None:
        return invitation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invitation with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a invitation",
    response_model=InvitationUpdate,
)
def update_invitation(id: UUID, invitation: InvitationUpdate = Body(...)):
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


@router.delete("/{id}", response_description="Delete a invitation plan")
def delete_invitation(id: str, response: Response):
    delete_result = db.invitations.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invitation with ID {id} not found",
    )
