from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict
import uuid


class Location(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
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
                "name": "Drink and Drown",
                "address": "1234 street",
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
