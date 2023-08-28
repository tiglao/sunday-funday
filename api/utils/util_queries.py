from pydantic import BaseModel
from queries.client import db

collection = db["accounts"]


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
