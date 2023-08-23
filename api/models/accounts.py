<<<<<<< HEAD
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
=======
from pydantic import BaseModel
from jwtdown_fastapi.authentication import Token


class LogOut(BaseModel):
    account_id: str


class LogIn(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class Account(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str
    avatar: str
    user_name: str
    id: str


class AccountUpdate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str
    avatar: str
>>>>>>> 86fb5d18c9f9c3be517833d054c07294ef3801fe


class DuplicateAccountError(ValueError):
    pass


class AccountIn(BaseModel):
<<<<<<< HEAD
    email: EmailStr
=======
>>>>>>> 86fb5d18c9f9c3be517833d054c07294ef3801fe
    username: str
    password: str
    full_name: str


class AccountOut(BaseModel):
    id: str
<<<<<<< HEAD
    email: str
=======
    username: str
>>>>>>> 86fb5d18c9f9c3be517833d054c07294ef3801fe
    full_name: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountForm(BaseModel):
<<<<<<< HEAD
    email: str
    password: str


# token parameter, creates token
=======
    username: str
    password: str


>>>>>>> 86fb5d18c9f9c3be517833d054c07294ef3801fe
class AccountToken(Token):
    account: AccountOut
    # pass
