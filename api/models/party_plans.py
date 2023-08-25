from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List
from datetime import date, datetime
from uuid import UUID


class PartyPlan(BaseModel):
    id: Optional[UUID]
    username: str
    notes: str
    date: date
    invitations: Optional[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    party_status: str
    keywords: List[str]
    general_location: str
    favorite_locations: Optional[Dict[str, str]]
    description: str
    image: Optional[HttpUrl]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "Billy1234",
                "notes": "Notes go here....",
                "date": "2022-02-22",
                "invitees": {
                    "name": "id",
                    "name": "id",
                    "name": "id",
                    "name": "id",
                },
                "start_time": "2022-02-22 14:30",
                "end_time": "2022-02-22 17:30",
                "party_status": "draft",
                "keywords": ["fun", "bar", "burgers"],
                "general_location": "Denver",
                "favorite_locations": {
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                },
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
            }
        }


class PartyPlanUpdate(BaseModel):
    username: Optional[str]
    notes: Optional[str]
    date: Optional[date]
    invitations: Optional[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    party_status: Optional[str]
    keywords: Optional[List[str]]
    general_location: Optional[str]
    favorite_locations: Optional[Dict[str, str]]
    chosen_locations: Optional[Dict[str, str]]
    description: Optional[str]
    image: Optional[HttpUrl]

    class Config:
        schema_extra = {
            "example": {
                "id": "generated",
                "username": "Billy1234",
                "notes": "Notes go here....",
                "date": "2022-02-22",
                "invitees": {
                    "name": "id",
                    "name": "id",
                    "name": "id",
                    "name": "id",
                },
                "start_time": "2022-02-22 14:30",
                "end_time": "2022-02-22 17:30",
                "party_status": "draft",
                "keywords": ["fun", "bar", "burgers"],
                "general_location": "Denver",
                "favorite_locations": {
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                },
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
            }
        }
