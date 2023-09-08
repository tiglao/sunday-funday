from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
DB_NAME = os.environ.get("DB_NAME")
client = MongoClient(DATABASE_URL)
db = client[DB_NAME]
invitations_collection = db["invitations"]
party_plans_collection = db["party_plans"]


def get_party_plan_by_id(party_plan_id):
    party_plan = party_plans_collection.find_one({"_id": party_plan_id})
    return party_plan
