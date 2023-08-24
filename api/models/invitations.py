from pydantic import BaseModel
from typing import Optional
from clients.client import client
from uuid import UUID, uuid4
from party_plans import PartyPlan
from datetime import datetime


class Invitation(BaseModel):
    id: Optional[UUID] = uuid4()
    account_id: str
    guest_name: str
    email: str
    party_plan: PartyPlan
    rsvp_status: Optional[bool] = None
    created_at: Optional[datetime] = datetime.now()

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "account_id": "76565765",
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
    account_id: Optional[str]
    rsvpStatus: Optional[bool]

    class Config:
        schema_extra = {
            "example": {"account_id": "76565765", "rsvpStatus": "False"}
        }
