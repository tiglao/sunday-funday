from typing import Optional, List
import googlemaps
from pydantic import BaseModel
import uuid
from types import GeneratorType
import responses


gmaps = googlemaps.Client(key = 'AIzaSyA-5Jr7-9Q53rLg1lTZc-vj1VOgRAHoHw8')

class Places(BaseModel):
    def setUp(self):
        address_components = Optional[List[str]]
        adr_address = Optional [str]
        fomatted_phone_number =  Optional [str]       
        icon =  Optional[str]
        place_id = str   
        rating = Optional[int]    
        types = Optional[List[str]] 
        website = Optional[str]
        review = [List[PlaceReview]] - #should be a foreign key
            PlaceReview ={
                "author_name": "John_Smith",
                "rating": "2",
                "relative_time_description": "2000-01-01T00:00:00",
                "time": "2000-01-01T00:00:00" #use DateTimeField
            }