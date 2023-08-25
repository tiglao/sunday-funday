<<<<<<< HEAD
=======
from pydantic import BaseModel, Field, validator
>>>>>>> 110c37f6d8ae545e573e65dd72255b4c19341f22
from datetime import datetime
from typing import Optional
from uuid import UUID

<<<<<<< HEAD
from pydantic import BaseModel, Field, validator


class Note(BaseModel):
    id: UUID
    created_time: datetime = Field(default_factory=datetime.utcnow)
    updated_time: Optional[datetime] = None
    comment: str
    account_id: str
    party_plan_id: Optional[str] = None
    location_id: Optional[str] = None
    # account_id: UUID
    # party_plan_id: Optional[UUID]
    # location_id: Optional[UUID]
=======

class Note(BaseModel):
    id: UUID
    created: datetime = Field(default_factory=datetime.utcnow)
    updated: Optional[datetime] = None
    comment: str
    account_id: str
    party_plan_id: Optional[UUID] = None
    location_id: Optional[UUID] = None
    # account_id: UUID
>>>>>>> 110c37f6d8ae545e573e65dd72255b4c19341f22

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "comment": "I like to code LOL",
                "account_id": "123e4567-e89b-12d3-a456-426614174001",  # example UUID
                "party_plan_id": "123e4567-e89b-12d3-a456-426614174002",  # example UUID
                "location_id": "123e4567-e89b-12d3-a456-426614174003",  # example UUID
            }
        }


class NoteCreate(BaseModel):
    comment: str
    account_id: UUID
    party_plan_id: Optional[str] = None
    location_id: Optional[str] = None

    @validator("location_id", pre=True, always=True)
    def check_exclusivity(cls, location_id, values):
        party_plan_id = values.get("party_plan_id")
        if location_id is not None and party_plan_id is not None:
            raise ValueError(
                "A note cannot be associated with both a location and a party plan."
            )
        return location_id

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "comment": "I sometimes like to code LOL",
                "party_plan_id": "123e4567-e89b-12d3-a456-426614174002",
            }
        }


<<<<<<< HEAD
# class NoteOut(BaseModel):
#     comment: str
#     account_id: UUID
#     party_plan_id: Optional[str] = None
#     location_id: Optional[str] = None

#     @validator("location_id", pre=True, always=True)
#     def check_exclusivity(cls, location_id, values):
#         party_plan_id = values.get("party_plan_id")
#         if location_id is not None and party_plan_id is not None:
#             raise ValueError("A note cannot be associated with both a location and a party plan.")
#         return location_id

#     class Config:
#         allow_population_by_field_name = True
#         schema_extra = {
#             "example": {
#                 "comment": "I sometimes like to code LOL",
#                 "party_plan_id": "123e4567-e89b-12d3-a456-426614174002",
#             }
#         }


=======
>>>>>>> 110c37f6d8ae545e573e65dd72255b4c19341f22
class NoteUpdate(BaseModel):
    updated_time: datetime
    note: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "updated_time": "2022-02-22T16:30:00",  # ISO 8601 format
                "comment": "I sometimes like to code LOL",
            }
        }
