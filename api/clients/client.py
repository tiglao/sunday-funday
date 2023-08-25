<<<<<<< HEAD
=======
from pymongo import MongoClient
from pymongo.common import UuidRepresentation
>>>>>>> 110c37f6d8ae545e573e65dd72255b4c19341f22
import os

from pymongo import MongoClient

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DB_NAME")

# client = MongoClient(DATABASE_URL)
# db = client[DB_NAME]

client = MongoClient(
    DATABASE_URL,  # uuidRepresentation=UuidRepresentation.STANDARD
    uuidRepresentation="standard",
)
db = client[DB_NAME]
