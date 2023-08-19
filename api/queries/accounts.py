from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Dict, Optional
from datetime import datetime
from queries.client import db
from uuid import UUID

collection = db["accounts"]


class DuplicateAccountError(ValueError):
    pass


class Account(BaseModel):
    id: UUID
    email: EmailStr
    username: str = Field(max_length=50)
    password: str
    full_name: Optional[str]
    dob: Optional[datetime]
    avatar: Optional[HttpUrl]
    party_plans: Optional[List[str]]
    invitations: Optional[List[str]]
    favorite_locations: Optional[List[str]]
    user_tags: Optional[List[str]]
    notes: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email": "example@email.com",
                "username": "sampleuser",
                "password": "password123",
                "full_name": "Sample User",
                "dob": "2000-01-01T00:00:00",
                "avatar": "http://example.com/image.jpg"
            }
        }

class AccountIn(BaseModel):
    email: EmailStr
    username: str = Field(max_length=50)
    password: str
    full_name: Optional[str]
    dob: Optional[datetime]
    avatar: Optional[HttpUrl]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "email": "example@email.com",
                "username": "sampleuser",
                "password": "password123",
                "full_name": "Sample User",
                "dob": "2000-01-01T00:00:00",
                "avatar": "http://example.com/image.jpg"
            }
        }



class AccountOut(BaseModel):
    id: UUID
    username: str
    full_name: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountRepo(BaseModel):
    def get(self, username: str) -> AccountOutWithPassword:
        acc = collection.find_one({"username": username})
        print
        if not acc:
            return None
        acc["id"] = str(acc["_id"])
        return AccountOutWithPassword(**acc)

    def create(
        self, info: AccountIn, hashed_password: str
    ) -> AccountOutWithPassword:
        info = info.dict()
        if self.get(info["username"]) is not None:
            raise DuplicateAccountError
        info["hashed_password"] = hashed_password
        del info["password"]
        collection.insert_one(info)
        id = str(info["_id"])
        acc = AccountOutWithPassword(**info, id=id)
        return acc
