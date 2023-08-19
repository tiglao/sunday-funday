import os
from pydantic import BaseModel
from fastapi import Depends
from jwtdown_fastapi.authentication import Authenticator
# from util_queries import AccountRepo, AccountOut, AccountOutWithPassword



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


class MyAuthenticator(Authenticator):
    async def get_account_data(
        self,
        username: str,
        accounts: AccountRepo,
    ):
        # Use your repo to get the account based on the
        # username (which could be an email)
        return accounts.get(username)

    def get_account_getter(
        self,
        accounts: AccountRepo = Depends(),
    ):
        # Return the accounts. That's it.
        return accounts

    def get_hashed_password(self, account: AccountOutWithPassword):
        # Return the encrypted password value from your
        # account object
        return account.hashed_password

    def get_account_data_for_cookie(self, account: AccountOut):
        # Return the username and the data for the cookie.
        # You must return TWO values from this method.
        return account.username, AccountOut(**account.dict())


authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])
