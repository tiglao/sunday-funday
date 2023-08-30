from clients.client import db
from models.accounts import (
    AccountIn,
    AccountOutWithPassword,
    DuplicateAccountError,
)
from pydantic import BaseModel

collection = db["accounts"]


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
