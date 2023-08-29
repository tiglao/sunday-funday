from pydantic import BaseModel
from jwtdown_fastapi.authentication import Token
from typing import Optional
from pydantic import BaseModel, EmailStr


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
    full_name: str
    date_of_birth: Optional[str] = None
    avatar: Optional[str] = None
    username: str


class AccountUpdate(BaseModel):
    full_name: Optional[str]
    date_of_birth: Optional[str]
    avatar: Optional[str]


class DuplicateAccountError(ValueError):
    pass


class AccountAll(BaseModel):
    email: Optional[str]
    full_name: Optional[str]
    date_of_birth: Optional[str]
    avatar: Optional[str]
    username: Optional[str]


class AccountOut(BaseModel):
    id: str
    username: str
    full_name: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountForm(BaseModel):
    username: str
    password: str


class AccountToken(Token):
    account: AccountOut
    # pass
