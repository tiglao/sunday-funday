from pydantic import BaseModel, Field
from typing import Optional
import uuid


class Invitation(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    account_id: str
    rsvpStatus: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "account_id": "76565765",
            }
        }


class InvitationUpdate(BaseModel):
    account_id: Optional[str]
    rsvpStatus: Optional[bool]

    class Config:
        schema_extra = {
            "example": {"account_id": "76565765", "rsvpStatus": "False"}
        }
