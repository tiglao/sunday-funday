from datetime import date, datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID

from locations import Location
from pydantic import BaseModel, Field, HttpUrl


class PartyStatus(str, Enum):
    DRAFT = "draft"
    SHARE_DRAFT = "share draft"
    FINALIZED = "finalized"


class ApiMapsLocation(BaseModel):
    geo: Optional[List[float]]
    input: Optional[str]


class PartyPlan(BaseModel):
    id: UUID
    account_id: str
    created: datetime
    updated: Optional[datetime]
    api_maps_location: List[ApiMapsLocation]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    description: Optional[str]
    image: Optional[HttpUrl]
    party_status: Optional[PartyStatus]
    invitations: Optional[List[UUID]]
    keywords: Optional[List[str]]
    searched_locations: Optional[List[Location]]
    favorite_locations: Optional[List[Location]]
    chosen_locations: Optional[List[Location]]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "account_id": "123456789",
                "created": "2022-02-22T14:30:00",
                "updated": "2022-02-22T16:30:00",
                "api_maps_location": [
                    {
                        "geo": {
                            "type": "Point",
                            "coordinates": [40.7128, -74.0060],
                            "expires": "2023-09-24T22:42:00.402000",
                        },
                        "input": "New York, NY",
                    }
                ],
                "start_time": "2022-02-22T14:30:00",
                "end_time": "2022-02-22T17:30:00",
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
                "party_status": "draft",
                "invitations": ["id1", "id2"],
                "keywords": ["fun", "bar", "burgers"],
                "searched_locations": [
                    "location_id1",
                    "location_id2",
                    "location_id3",
                ],
                "favorite_locations": ["location_id1", "location_id2"],
                "chosen_locations": ["location_id2"],
            }
        }


class PartyPlanCreate(BaseModel):
    # id, account_id, created, party_status auto-generated
    account_id: str
    api_maps_location: List[ApiMapsLocation]
    start_time: datetime
    end_time: Optional[datetime]
    description: Optional[str]
    image: Optional[HttpUrl]
    keywords: Optional[List[str]]

    class Config:
        schema_extra = {
            "example": {
                "account_id": "123456789",
                "api_maps_location": [
                    {
                        "input": "New York, NY",
                    }
                ],
                "start_time": "2022-02-23T14:30:00",
                "end_time": "2022-02-23T17:30:00",
                "description": "Updated Description here ....",
                "image": "https://picsum.photos/201",
                "keywords": ["party", "drinks", "dance"],
            }
        }


class PartyPlanUpdate(BaseModel):
    api_maps_location: Optional[List[ApiMapsLocation]]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    description: Optional[str]
    image: Optional[HttpUrl]
    invitations: Optional[List[UUID]]
    party_status: Optional[PartyStatus]
    keywords: Optional[List[str]]
    searched_locations: Optional[List[Location]]
    favorite_locations: Optional[List[Location]]
    chosen_locations: Optional[List[Location]]

    class Config:
        schema_extra = {
            "example": {
                "api_maps_location": [
                    {
                        "geo": {
                            "type": "Point",
                            "coordinates": [40.7128, -74.0060],
                        },
                        "input": "New York, NY",
                    }
                ],
                "start_time": "2022-02-23T14:30:00",
                "end_time": "2022-02-23T17:30:00",
                "description": "Updated Description here ....",
                "image": "https://picsum.photos/201",
                "party_status": "share draft",
                "invitations": ["<INSERT VALID INVITATION"],
                "keywords": ["party", "drinks", "dance"],
                "searched_locations": [
                    "<placeid1 REPLACE ME>",
                    "<placeid2 REPLACE ME>",
                ],
                "favorite_locations": [
                    "<placeid1 REPLACE ME>",
                    "<placeid2 REPLACE ME>",
                ],
                "chosen_locations": ["<placeid2 REPLACE ME>"],
            }
        }
