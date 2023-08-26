from pydantic import BaseModel
from typing import Optional, List, Dict
from uuid import UUID


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
    account_id: str
    rsvp_status: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "account_id": "123e4567-e89b-12d3-a456-426614174001",
                "rsvp_status": False,
            }
        }


class InvitationUpdate(BaseModel):
    rsvp_status: Optional[bool]

    class Config:
        schema_extra = {"example": {"rsvp_status": True}}
