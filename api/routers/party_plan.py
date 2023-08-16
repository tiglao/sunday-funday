from fastapi import APIRouter, Body, HTTPException, status, Response, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID
from authenticator import authenticator
from queries.party_plan import PartyPlan, PartyPlanUpdate
from queries.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new party",
    status_code=status.HTTP_201_CREATED,
    response_model=PartyPlan,
)
def create_partyplan(
    plan: PartyPlan = Body(...),
    account: dict = Depends(authenticator.get_current_account_data),
):
    plan = jsonable_encoder(plan)
    new_plan = db.party_plan.insert_one(plan)
    created_plan = db.party_plan.find_one({"_id": new_plan.inserted_id})
    created_plan["_id"] = str(created_plan["_id"])
    return created_plan


@router.get(
    "/",
    response_description="List all parties",
    response_model=List[PartyPlan],
)
def list_partyplan(
    account: dict = Depends(authenticator.get_current_account_data),
):
    parties = list(db.party_plan.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single party by id",
    response_model=PartyPlan,
)
def find_party(
    id: str,
    account: dict = Depends(authenticator.get_current_account_data),
):
    if (party := db.party_plan.find_one({"_id": id})) is not None:
        return party
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Party with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a party",
    response_model=PartyPlanUpdate,
)
def update_party(
    id: UUID,
    party: PartyPlanUpdate = Body(...),
    account: dict = Depends(authenticator.get_current_account_data),
):
    existing_party = db.party_plan.find_one({"_id": str(id)})

    if not existing_party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with ID {id} not found",
        )

    if party.startTime:
        party.date = party.date.isoformat()

    party_data = {k: v for k, v in party.dict().items() if v is not None}

    if party_data:
        db.party_plan.update_one({"_id": str(id)}, {"$set": party_data})

    return db.party_plan.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete a party plan")
def delete_party(
    id: str,
    response: Response,
    account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.party_plan.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Party with ID {id} not found",
    )
