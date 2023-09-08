from pydantic import BaseModel, Field
from typing import Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime

# needs to pull in account full name (no first name, use method to split string) account email


class Invitation(BaseModel):
    id: UUID
    created: datetime
    updated: Optional[datetime]
    account: Dict[str, str]
    party_plan_id: UUID
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
    id: Optional[UUID] = Field(default_factory=uuid4)
    account_id: str
    guest_name: str
    email: str
    party_plan_id: UUID
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    def model_dump(self):
        return {
            "id": str(self.id),
            "account_id": self.account_id,
            "guest_name": self.guest_name,
            "email": self.email,
            "created_at": self.created_at,
        }

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


class InvitationUpdate(BaseModel):
    sent_status: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "rsvp_status": "yes",
                "sent_status": True,
            }
        }


class InvitationPayload(BaseModel):
    fullName: str
    email: str


# user inputs emails (has email strings that are associated with account).


# from server to user // later
# when an invitation is sent, it checks to see if the user has the email in their address book. if an account is associated with the email, it will just send from there.

# now// from server to user// caveat
# user will need to enter in all emails.

# when an invitation is sent, it checks to see if the user exists.

#
