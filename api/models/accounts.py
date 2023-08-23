from pydantic import BaseModel, EmailStr
from jwtdown_fastapi.authentication import Token
from typing import Optional, List, Dict, Union
from uuid import UUID
from datetime import datetime, date


# class LogOut(BaseModel):
#     account_id: str


# class LogIn(BaseModel):
#     email: str
#     password: str
#     first_name: str
#     last_name: str


# favorite locations is a dictionary list of location_ids and user's associated categories
# notes is a list of user comments with associated party_plan or location
class Account(BaseModel):
    id: UUID
    created: datetime
    updated: datetime
    email: EmailStr
    username: str
    password: str
    full_name: str
    dob: Optional[date]
    avatar: Optional[HttpUrl]
    party_plan_ids: Optional[List[UUID]]
    invitation_ids: Optional[List[UUID]]
    favorite_locations: Optional[List[Dict[str, Union[str, List[str]]]]]
    notes: Optional[List[Dict[str, Union[str, List[str]]]]]
    active_status: bool = True


class AccountCreate(BaseModel):
    pass


class AccountUpdate(BaseModel):
    pass


class DuplicateAccountError(ValueError):
    pass


class AccountIn(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str


class AccountOut(BaseModel):
    id: str
    email: str
    full_name: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountForm(BaseModel):
    email: str
    password: str


# token parameter, creates token
class AccountToken(Token):
    account: AccountOut
    # pass
