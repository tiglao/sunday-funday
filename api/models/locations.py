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
