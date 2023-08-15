from typing import Literal
import pydantic from BaseModel
from typing import List


class Rsvp(BaseModel): 
    yes_no: bool

class PartyEventList(BaseModel):  #come back and look at this model#
    events: List[LocationList]
    invitees: List[InviteesList]
    date: str
    time: str


class Invitees(BaseModel):
   first_name: str
   last_name: str
   email_address: str
   phone_number:str 


class InviteesList(BaseModel):
    status: Literal[
        "Yes",
        "No",
        "Viewed",
    ]
    first_name:str
    last_name:str
    email_address: str
    phone_number:str


class PartyPlans(BaseModel):
    username: str
    notes:str
    date: str 
    invitees: List[InviteesList]
    start_time:str
    end_time:str
    party_status:str
    keywords: str
    general_location: str
    favorite_locations: List[FavoriteLocations]



class FavoriteLocations(BaseModel):
    description: str
    picture: str #url
    start_time:str



