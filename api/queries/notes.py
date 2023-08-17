from pydantic import BaseModel, Field
from typing import Optional
import uuid


class Note(BaseModel):
    id: str = Field(
        default_factory=uuid.uuid4,
        alias="_id"
    )
    created_time: str
    updated_time: str
    note: str
    account_id: str
    party_plan_id: str
    location_id: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "created_time": "2022-02-22 14:30",
                "updated_time": "2022-02-22 14:30",
                "note": "I like to code LOL",
                "account_id": "76565765",
                "party_plan_id": "000001",
                "location_id": "333",
            }
        }


class NoteUpdate(BaseModel):
    updated_time: str
    note: str

    class Config:
        schema_extra = {
            "example": {
                "updated_time": "2022-02-22 16:30",
                "note": "I sometimes like to code LOL",
            }
        }
