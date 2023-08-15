from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class Location(BaseModel):
    place_id: str
    name: str
    address: str
    lat: float
    lon: float
    type: str ????
    category: str
    favoriteStatus: Optional[bool] = Field(None, description = "empty until selection process. all not favorited = False")
    notes: Optional[str] = Field(None, description = "collection of multiple comments about the location")
    hoursOfOperation: Optional[dict] = Field(None, description="dictionary with days as keys")
    website: Optional[HttpUrl]
    image: Optional[HttpUrl]

class LocationList(BaseModel):
    locations: List[Location]
