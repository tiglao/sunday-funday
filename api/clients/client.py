from pymongo import MongoClient
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("sunday_funday")

client = MongoClient(DATABASE_URL)
db = client[DB_NAME]


def get_database():
    client = MongoClient("mongodb://root:example@mongo:27017")
    db = client['sunday_funday']
    return db
