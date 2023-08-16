from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from datetime import date, datetime
import uuid


class PartyPlan(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    notes: str
    date: date
    invitees: Dict[str, str]
    startTime: datetime
    endTime: datetime
    partyStatus: str
    keywords: List[str]
    generalLocation: str
    favoriteLocations: Dict[str, str]
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
                "startTime": "2022-02-22 14:30",
                "endTime": "2022-02-22 17:30",
                "partyStatus": "draf",
                "keywords": ["fun", "bar", "burgers"],
                "generalLocation": "Denver",
                "favoriteLocations": {
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
    invitees: Optional[Dict[str, str]]
    startTime: datetime
    endTime: datetime
    partyStatus: Optional[str]
    keywords: Optional[List[str]]
    generalLocation: Optional[str]
    favoriteLocations: Optional[Dict[str, str]]
    description: Optional[str]
    image: Optional[HttpUrl]

    class Config:
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
                "startTime": "2022-02-22 14:30",
                "endTime": "2022-02-22 17:30",
                "partyStatus": "draf",
                "keywords": ["fun", "bar", "burgers"],
                "generalLocation": "Denver",
                "favoriteLocations": {
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                },
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
            }
        }
