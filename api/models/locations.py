from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl


class Location(BaseModel):
    place_id: str
    account_location_tags: Optional[Dict[str, List[str]]]
    notes: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {

                "place_id": "76565765",
                "account_location_tags": {
                    "123e4567-e89b-12d3-a456-426614174001": {"tag1", "tag2"},
                    "123e4567-e89b-12d3-a456-426614174002": {"tag3"},
                },
                "notes" : "notes 1"
            }
        }


class LocationCreate(BaseModel):
    place_id: str
    account_location_tags: Optional[Dict[str, List[str]]]

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
    favorite_status: bool = False
    account_ids: List[str] = []
    account_location_tags: Optional[Dict[str, List[str]]]
    notes: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "general_location": "Denver",
                "party_date": "2022-02-23",
                "start_time": "2022-02-23T14:30:00",
                "end_time": "2022-02-23T17:30:00",
                "description": "Updated Description here ....",
                "image": "https://picsum.photos/201",
                "party_status": "share draft",
                "invitations": {"name3": "id3", "name4": "id4"},
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


# class Location(BaseModel):
#     place_id: str
#     name: str
#     address: str
#     lat: float
#     lon: float
#     type: str
#     category: str
#     favoriteStatus: Optional[bool] = Field(None, description = "empty until selection process. all not favorited = False")
#     notes: Optional[str] = Field(None, description = "collection of multiple comments about the location")
#     hoursOfOperation: Optional[dict] = Field(None, description="dictionary with days as keys")
#     website: Optional[HttpUrl]
#     image: Optional[HttpUrl]

# class LocationList(BaseModel):
#     locations: List[Location]
