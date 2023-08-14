from pydantic import BaseModel
from typing import List


class Location(BaseModel):
    type: str
    coordinates: List[float] #reference Google Maps API for inputs#
    notes: str

class LocationList(BaseModel):
    locations: List[Location]