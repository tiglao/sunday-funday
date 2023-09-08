import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.common import UuidRepresentation

load_dotenv()


from pymongo import MongoClient

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(
    DATABASE_URL,
    uuidRepresentation="standard",
)
db = client[DB_NAME]
