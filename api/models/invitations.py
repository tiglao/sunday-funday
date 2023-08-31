from pydantic import BaseModel
from typing import Optional, Dict
from clients.client import client
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum


# needs to pull in account full name (no first name, use method to split string) account email


class RsvpStatus(str, Enum):
    YES = "yes"
    MAYBE = "maybe"
    NO = "no"


class Invitation(BaseModel):
    id: UUID
    created: datetime
    updated: Optional[datetime]
    account: Dict[str, str]
    party_plan_id: UUID
    rsvp_status: Optional[RsvpStatus]
    sent_status: Optional[bool]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "created": "2023-08-28T14:12:12Z",
                "updated": "2023-08-28T16:12:12Z",
                "account": {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "fullname": "John Doe",
                    "email": "john.doe@example.com",
                },
                "party_plan_id": "123e4567-e89b-12d3-a456-426614174002",
                "rsvp_status": "yes",
                "sent_status": True,
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
# class InvitationCreate(BaseModel):
#     account: Dict[str, str]

#     class Config:
#         allow_population_by_field_name = True
#         schema_extra = {
#             "example": {
#                 "account": {
#                     "id": "123e4567-e89b-12d3-a456-426614174001",
#                     "fullname": "John Doe",
#                     "email": "john.doe@example.com",
#                 }
#             }
#         }


def get_invitation_by_id(invitation_id: UUID):
    return client.db.invitations.find_one({"_id": invitation_id})


def update_invitation_rsvp(invitation_id: UUID, status: bool):
    client.db.invitations.update_one(
        {"_id": invitation_id},
        {"$set": {"rsvpStatus": status}}
    )


class InvitationUpdate(BaseModel):
    rsvp_status: Optional[RsvpStatus]
    sent_status: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "rsvp_status": "yes",
                "sent_status": True,
            }
        }


# user inputs emails (has email strings that are associated with account).


# from server to user // later
# when an invitation is sent, it checks to see if the user has the email in their address book. if an account is associated with the email, it will just send from there.

# now// from server to user// caveat
# user will need to enter in all emails.

# when an invitation is sent, it checks to see if the user exists.

#
