from fastapi import APIRouter, Body, HTTPException, status, Response, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID, uuid4
from utils.authenticator import authenticator
from models.party_plans import PartyPlan, PartyPlanUpdate
from clients.client import db\
from maps_api import geo_code, g_key
from datetime import datetime

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new party plan",
    status_code=status.HTTP_201_CREATED,
    response_model=PartyPlan,
)
def create_party_plan(
    party_plan: PartyPlan = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # Generate id, timestamp, default status of draft
    party_plan_data = jsonable_encoder(party_plan)
    party_plan_data["id"] = str(uuid4())
    party_plan_data["created"] = datetime.now()
    party_plan_data["party_status"] = "draft"

    # Geocode the general_location
    address = party_plan.get("general_location", "")
    if address:
        geo_data = geo_code(address, g_key)
        if geo_data:
            party_plan_data["latitude"] = geo_data["lat"]
            party_plan_data["longitude"] = geo_data["lng"]

    # Add to the database
    new_party_plan = db.party_plans.insert_one(party_plan_data)
    if not new_party_plan.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add party plan to the database.",
        )

    # Fetch the plan you just made
    created_party_plan = db.party_plans.find_one({"id": party_plan_data["id"]})
    if not created_party_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party plan with ID {party_plan_data['id']} not found after insertion.",
        )

    return created_party_plan


@router.get(
    "/",
    response_description="List all party plans",
    response_model=List[PartyPlan],
)
def list_party_plans(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    parties = list(db.party_plan.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single party plan by ID",
    response_model=PartyPlan,
)
def find_party_plan(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (party := db.party_plan.find_one({"_id": id})) is not None:
        return party
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Party with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a party plan",
    response_model=PartyPlanUpdate,
)
def update_party_plan(
    id: UUID,
    party: PartyPlanUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_party = db.party_plan.find_one({"_id": str(id)})

    if not existing_party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with ID {id} not found",
        )

    if party.start_time:
        party.date = party.date.isoformat()

    party_data = {k: v for k, v in party.dict().items() if v is not None}

    if party_data:
        db.party_plan.update_one({"_id": str(id)}, {"$set": party_data})

    return db.party_plan.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete a party plan")
def delete_party_plan(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.party_plan.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Party plan with id {id}) successfully deleted.",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No party plan with ID {id} found. Deletion incomplete.",
    )
