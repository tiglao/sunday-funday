from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Optional, Dict
from uuid import UUID

from models.invitations import Invitation, RsvpStatus


# needs to pull in account full name (no first name, use method to split string) account email


class SentStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    OPENED = "opened"


class EmailContext(BaseModel):
    invitation_id: UUID
    created_at: datetime  # use information from invitation created
    updated_at: Optional[datetime]  # use information from invitation updated
    account: Dict[str, str]
    party_plan_id: UUID
    rsvp_status: Optional[RsvpStatus]
    sent_status: SentStatus  # should be a limited number of types of statuses


class ApiEmail(BaseModel):
    id: UUID
    to: str
    subject: str
    template: str
    api_context: EmailContext

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "to": "John Doe <john.doe@example.com>",
                "subject": "Your Invitation",
                "template": "invitation_template",
                "api_context": {
                    "invitation_id": "123e4567-e89b-12d3-a456-426614174001",
                    "created_at": "2023-08-28T14:12:12Z",
                    "updated_at": "2023-08-28T16:12:12Z",
                    "account": {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "fullname": "John Doe",
                        "email": "john.doe@example.com",
                    },
                    "party_plan_id": "123e4567-e89b-12d3-a456-426614174002",
                    "rsvp_status": "yes",
                    "sent_status": "sent",
                },
            }
        }
