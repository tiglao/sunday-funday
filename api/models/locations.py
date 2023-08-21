from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict
from uuid import UUID


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
    favorite_status: bool = False
    account_id: str
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
                "note_ids": [
                    "note1",
                    "note2",
                ],
                "favorite_status": True,
                "account_ids": ["account1", "account2"],
                "account_location_tags": {
                    "account1": ["tag1", "tag2"],
                    "account2": ["tag3"],
                },
            }
        }
