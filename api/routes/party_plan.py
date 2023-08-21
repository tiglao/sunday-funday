from fastapi import APIRouter, Body, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID
<<<<<<<< HEAD:api/routes/party_plan.py

from queries.party_plan import PartyPlan, PartyPlanUpdate
from queries.client import db
========
from utils.authenticator import authenticator
from models.party_plans import PartyPlan, PartyPlanUpdate
from clients.client import db
>>>>>>>> 6b018ad (Auth refactor):api/routers/party_plans.py


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new party plan",
    status_code=status.HTTP_201_CREATED,
    response_model=PartyPlan,
)
<<<<<<<< HEAD:api/routes/party_plan.py
def create_partyplan(plan: PartyPlan = Body(...)):
========
def create_party_plan(
    plan: PartyPlan = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
>>>>>>>> 6b018ad (Auth refactor):api/routers/party_plans.py
    plan = jsonable_encoder(plan)
    new_plan = db.party_plan.insert_one(plan)
    created_plan = db.party_plan.find_one({"_id": new_plan.inserted_id})
    created_plan["_id"] = str(created_plan["_id"])
    return created_plan


@router.get(
    "/",
    response_description="List all party plans",
    response_model=List[PartyPlan],
)
<<<<<<<< HEAD:api/routes/party_plan.py
def list_partyplan():
========
def list_party_plans(
    # account: dict = Depends(authenticator.get_current_account_data),
):
>>>>>>>> 6b018ad (Auth refactor):api/routers/party_plans.py
    parties = list(db.party_plan.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single party plan by ID",
    response_model=PartyPlan,
)
def find_party_plan(
    id: str,
<<<<<<<< HEAD:api/routes/party_plan.py
========
    # account: dict = Depends(authenticator.get_current_account_data),
>>>>>>>> 6b018ad (Auth refactor):api/routers/party_plans.py
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
<<<<<<<< HEAD:api/routes/party_plan.py
def update_party(id: UUID, party: PartyPlanUpdate = Body(...)):
========
def update_party_plan(
    id: UUID,
    party: PartyPlanUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
>>>>>>>> 6b018ad (Auth refactor):api/routers/party_plans.py
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
<<<<<<<< HEAD:api/routes/party_plan.py
def delete_party(id: str, response: Response):
========
def delete_party_plan(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
>>>>>>>> 6b018ad (Auth refactor):api/routers/party_plans.py
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
