from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from datetime import date, datetime
from uuid import UUID
from enum import Enum


class PartyStatus(str, Enum):
    DRAFT = "draft"
    SHARE_DRAFT = "share draft"
    FINALIZED = "finalized"


class PartyPlan(BaseModel):
    id: UUID
    account_id: str
    created: datetime
    updated: Optional[datetime]
    general_location: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    description: Optional[str]
    image: Optional[HttpUrl]
    party_status: PartyStatus
    invitations: Optional[List[UUID]]
    keywords: Optional[List[str]]
    favorite_locations: Optional[Dict[str, str]]
    chosen_locations: Optional[Dict[str, str]]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "account_id": "123456789",
                "created": "2022-02-22T14:30:00",
                "updated": "2022-02-22T16:30:00",
                "general_location": "Denver",
                "start_time": "2022-02-22T14:30:00",
                "end_time": "2022-02-22T17:30:00",
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
                "party_status": "draft",
                "invitations": ["id1", "id2"],
                "keywords": ["fun", "bar", "burgers"],
                "favorite_locations": {
                    "location1": "place_id1",
                    "location2": "place_id2",
                },
                "chosen_locations": {
                    "locationA": "place_idA",
                    "locationB": "place_idB",
                },
            }
        }


class PartyPlanCreate(BaseModel):
    # id, account_id, created, party_status auto-generated
    account_id: str
    general_location: str
    start_time: datetime
    end_time: Optional[datetime]
    description: Optional[str]
    image: Optional[HttpUrl]
    keywords: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "general_location": "Denver, CO",
                "account_id": "123456789",
                "start_time": "2022-02-23T14:30:00",
                "end_time": "2022-02-23T17:30:00",
                "description": "Updated Description here ....",
                "image": "https://picsum.photos/201",
                "invitations": [
                    "<CHANGE THIS IT NEEDS TO BE A VALID INVITATION ID>"
                ],
                "keywords": ["party", "drinks", "dance"],
            }
        }


class PartyPlanUpdate(BaseModel):
    general_location: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    description: Optional[str]
    image: Optional[HttpUrl]
    invitations: Optional[List[UUID]]
    party_status: PartyStatus
    keywords: Optional[List[str]]
    favorite_locations: Optional[Dict[str, str]]
    chosen_locations: Optional[Dict[str, str]]

    class Config:
        schema_extra = {
            "example": {
                "general_location": "Denver",
                "start_time": "2022-02-23T14:30:00",
                "end_time": "2022-02-23T17:30:00",
                "description": "Updated Description here ....",
                "image": "https://picsum.photos/201",
                "party_status": "share draft",
                "invitations": ["<INSERT VALID INVITATION"],
                "keywords": ["party", "drinks", "dance"],
                "favorite_locations": {
                    "new_location1": "new_place_id1",
                    "new_location2": "new_place_id2",
                },
                "chosen_locations": {
                    "new_locationX": "new_place_idX",
                    "new_locationY": "new_place_idY",
                },
            }
        }
