from pymongo import MongoClient
from pymongo.common import UuidRepresentation
import os
from dotenv import load_dotenv

load_dotenv()


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
