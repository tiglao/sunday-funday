from pymongo import MongoClient
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DATABASE_URL")

client = MongoClient(DATABASE_URL)
db = client[DB_NAME]


def get_database():
    client = MongoClient(DATABASE_URL)
    db = client['DATABASE_URL']
    return db
