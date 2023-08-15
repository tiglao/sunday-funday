from pydantic import BaseModel



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
    id:str

class AccountUpdate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str
    avatar: str

