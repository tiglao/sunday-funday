from fastapi import APIRouter, Body, HTTPException, status, Response, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from utils.authenticator import authenticator
from queries.accounts import Account, AccountIn, AccountOut
from queries.client import db


router = APIRouter()


collection = db["accounts"]


class DuplicateAccountError(ValueError):
    pass


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


@router.post(
    "/",
    response_description="Create a new account",
    status_code=status.HTTP_201_CREATED,
    response_model=AccountOut,
)
def create_account(
    account: AccountIn = Body(...),
):
    account_dict = jsonable_encoder(account)
    account_dict["id"] = str(uuid4())
    new_account = db.accounts.insert_one(account_dict)
    created_account = db.accounts.find_one(
        {"_id": new_account.inserted_id}
    )
    created_account["_id"] = str(created_account["_id"])
    return created_account


@router.get(
    "/",
    response_description="List all accounts",
    response_model=List[Account],
)
\
def list_accounts(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    accounts = list(db.accounts.find(limit=100))
    print("what you get", accounts)
    for account in accounts:
        account["id"] = str(account["_id"])
    return accounts


@router.get(
    "/{id}",
    response_description="Get a single account by ID",
    response_model=Account,
)
def find_account(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (account := db.accounts.find_one({"_id": id})) is not None:
        return account
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Account with ID {id} not found",
    )
