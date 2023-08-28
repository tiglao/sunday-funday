from pydantic import BaseModel
from typing import Optional, List, Dict
from clients.client import client
from uuid import UUID, uuid4
from datetime import datetime


class Invitation(BaseModel):
    id: UUID
    account_id: str
    party_plan_id: UUID
    rsvp_status: bool = False
    # account_id: UUID
    # party_plan: UUID

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "account_id": "123e4567-e89b-12d3-a456-426614174001",
                "party_plan_id": "123e4567-e89b-12d3-a456-426614174002",
                "rsvp_status": False,
            }
        }


class InvitationCreate(BaseModel):
    id: Optional[UUID] = uuid4()
    account_id: str
    rsvp_status: bool = False
    guest_name: str
    email: str
    rsvp_status: Optional[bool] = None
    created_at: Optional[datetime] = datetime.now()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "account_id": "123e4567-e89b-12d3-a456-426614174001",
                "rsvp_status": False,
            }
        }


def get_invitation_by_id(invitation_id: UUID):
    return client.db.invitations.find_one({"_id": invitation_id})


def update_invitation_rsvp(invitation_id: UUID, status: bool):
    client.db.invitations.update_one(
        {"_id": invitation_id},
        {"$set": {"rsvpStatus": status}}
    )


class InvitationUpdate(BaseModel):
    rsvp_status: Optional[bool]

    class Config:
        schema_extra = {"example": {"rsvp_status": True}}
