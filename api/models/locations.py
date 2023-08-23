from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Union
from uuid import UUID


# people can favorite locations, so what should happen is that each location has a set of account ids that have favorited this location along with the location_tags they've chosen for the specific location.
class Location(BaseModel):
    id: UUID
    place_id: str
    note_ids: Optional[List[str]]
    favorite_status: bool = False
    party_plans: Optional[List[str]]
    user_tags: Optional[List[Dict[str, Union[str, List[str]]]]]

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
                "user_tags": [
                    {
                        "account_id": "123e4567-e89b-12d3-a456-426614174001",
                        "tags": ["tag1", "tag2"],
                    },
                    {
                        "account_id": "123e4567-e89b-12d3-a456-426614174002",
                        "tags": ["tag3"],
                    },
                ],
            }
        }


class LocationCreate(BaseModel):
    place_id: str
    favorite_status: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "place_id": "76565765",
                "favorite_status": False,
            }
        }


class LocationUpdate(BaseModel):
    note_ids: Optional[List[str]]
    favorite_status: Optional[bool]
    party_plans: Optional[List[str]]
    user_tags: Optional[List[Dict[str, Union[str, List[str]]]]]

    class Config:
        schema_extra = {
            "example": {
                "note_ids": [
                    "123e4567-e89b-12d3-a456-426614174001",
                    "123e4567-e89b-12d3-a456-426614174002",
                ],
                "favorite_status": False,
                "party_plans": ["123e4567-e89b-12d3-a456-426614174001"],
                "user_tags": [
                    {
                        "account_id": "123e4567-e89b-12d3-a456-426614174001",
                        "tags": ["tag1", "tag2"],
                    },
                ],
            }
        }
