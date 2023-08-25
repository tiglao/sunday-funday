from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class Location(BaseModel):
    id: UUID
    place_id: str
    note_ids: Optional[List[str]]
    favorite_status: bool = False
    account_ids: List[str] = []
    account_location_tags: Optional[Dict[str, List[str]]]
    # note_ids: Optional[List[UUID]]
    # favorite_status: bool = False
    # account_ids: List[UUID]
    # account_location_tags: Optional[Dict[UUID, List[str]]]
    # account_ids: List[UUID]
    # account_location_tags: Optional[Dict[UUID, List[str]]]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",  # example UUID
                "place_id": "76565765",
                "note_ids": [
                    "123e4567-e89b-12d3-a456-426614174001",
                    "123e4567-e89b-12d3-a456-426614174002",
                ],
                "favorite_status": True,
                "account_ids": ["123e4567-e89b-12d3-a456-426614174001"],
                "account_location_tags": {
                    "123e4567-e89b-12d3-a456-426614174001": {"tag1", "tag2"},
                    "123e4567-e89b-12d3-a456-426614174002": {"tag3"},
                },
            }
        }


class LocationCreate(BaseModel):
    place_id: str
    name: str
    address: str
    type: str
    category: str
    favorite_status: bool = False
    notes: Optional[str]
    hours_of_operation: Optional[Dict[str, str]]
    website: Optional[HttpUrl]
    image: Optional[HttpUrl]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "place_id": "76565765",
                "favorite_status": True,
                "account_id": "123e4567-e89b-12d3-a456-426614174001",  # example UUID
                "account_location_tags": {
                    "123e4567-e89b-12d3-a456-426614174001": ["tag1", "tag2"],
                },
            }
        }


class LocationUpdate(BaseModel):
    place_id: Optional[str]
    name: Optional[str]
    address: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    type: Optional[str]
    category: Optional[str]
    favoriteStatus: Optional[bool]
    notes: Optional[str]
    hoursOfOperation: Optional[dict]
    website: Optional[HttpUrl]
    image: Optional[HttpUrl]

    class Config:
        schema_extra = {
            "example": {
                "place_id": "76565765",
                "name": "Drink and Drown",
                "address": "1234 street",
                "lat": "12242",
                "lon": "17043",
                "type": "?????",
                "category": "Bars",
                "notes": "...",
                "hoursOfOperation": {
                    "Monday": "9am - 8pm",
                    "Tuesday": "9am - 8pm",
                    "Wednesday": "9am - 8pm",
                    "Thursday": "9am - 8pm",
                    "Friday": "9am - 8pm",
                    "Saturday": "9am - 8pm",
                },
                "website": "https://www.google.com",
                "image": "https://picsum.photos/200",
            }
        }


# class Location(BaseModel):
#     place_id: str
#     name: str
#     address: str
#     lat: float
#     lon: float
#     type: str ????
#     category: str
#     favoriteStatus: Optional[bool] = Field(None, description = "empty until selection process. all not favorited = False")
#     notes: Optional[str] = Field(None, description = "collection of multiple comments about the location")
#     hoursOfOperation: Optional[dict] = Field(None, description="dictionary with days as keys")
#     website: Optional[HttpUrl]
#     image: Optional[HttpUrl]

# class LocationList(BaseModel):
#     locations: List[Location]
