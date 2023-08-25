import os

from pymongo import MongoClient

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
