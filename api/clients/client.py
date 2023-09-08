from uuid import UUID
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DB_NAME")
print("DATABASE_URL:", DATABASE_URL)
print("DB_NAME:", DB_NAME)

# client = MongoClient(DATABASE_URL)
# db = client[DB_NAME]

client = MongoClient(
    DATABASE_URL,  # uuidRepresentation=UuidRepresentation.STANDARD
    uuidRepresentation="standard",
)
db = client[DB_NAME]
invitations_collection = db["invitations"]


def get_database():
    client = MongoClient(DATABASE_URL)
    db = client[DB_NAME]
    return db
