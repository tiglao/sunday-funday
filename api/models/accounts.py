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


class DuplicateAccountError(ValueError):
    pass


class AccountIn(BaseModel):
    username: str
    password: str
    full_name: str


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
