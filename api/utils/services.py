from pymongo import MongoClient
from models.party_plans import PartyPlan
from dotenv import load_dotenv
from clients.client import db
import os

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME")


def update_rsvp_count_in_party_plan(party_plan_id: str, new_rsvp_count: int):
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    party_plans_collection = db['party_plans']

    query = {"_id": party_plan_id}
    update = {"$set": {"rsvp_count": new_rsvp_count}}

    result = party_plans_collection.update_one(query, update)

    if result.matched_count:
        return {"status": "success", "message": "RSVP count updated successfully"}
    else:
        return {"status": "failure", "message": "Could not find a party plan with the given ID"}


def get_latest_party_plan_by_id(party_plan_id: str) -> dict:
    party_plans_collection = db['party_plans']
    party_plan = party_plans_collection.find_one({"_id": party_plan_id})
    return party_plan


def calculate_latest_rsvp_count(party_plan: dict) -> int:
    # Assuming 'rsvp_count' is a field in your party_plan document
    current_rsvp_count = party_plan.get('rsvp_count', 0)
    new_rsvp_count = current_rsvp_count + 1  # Increment by 1; adjust as needed
    return new_rsvp_count
