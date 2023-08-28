from fastapi import APIRouter, Body, HTTPException, status, Response, Depends
from datetime import datetime
from typing import List
from datetime import datetime
from uuid import UUID, uuid4
from bson.binary import Binary
from datetime import datetime, timedelta
from utils.authenticator import authenticator
from models.party_plans import ApiMapsLocation, GeoJSON, PartyPlan, PartyPlanUpdate, PartyPlanCreate
from clients.client import db
from maps_api import geo_code
from fastapi.encoders import jsonable_encoder
import googlemaps
from api_keys import API_KEY



g_key = googlemaps.Client(key=API_KEY)



router = APIRouter()


@router.post(
    "/",
    response_description="Create a new party plan",
    status_code=status.HTTP_201_CREATED,
    response_model=PartyPlan,
)
def create_party_plan(
    party_plan: PartyPlanCreate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # generate id, timestamp, default status of draft
    party_plan_data = jsonable_encoder(party_plan)
    party_plan_data["id"] = str(uuid4())
    party_plan_data["created"] = datetime.now()
    party_plan_data["party_status"] = "draft"

    # Geocode the general_location
    address =  party_plan_data["api_maps_location"][0]["input"]
    if address:
        geo_data = geo_code(address,g_key)
        if geo_data:
            party_plan_data["api_maps_location"]["geo"]["coordinates"] = geo_data



    # Add to the database
    new_party_plan = db.party_plans.insert_one(party_plan_data)
    if not new_party_plan.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add party plan to database.",
        )

    # fetch the plan you just made
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
    party_plans = list(db.party_plans.find(limit=100))
    for party in party_plans:
        # fetch associated invitations
        invitations = list(db.invitations.find({"party_plan_id": party["id"]}))
        # return list of invitation ids
        party["invitations"] = [inv["id"] for inv in invitations]
    return party_plans


@router.get(
    "/{id}",
    response_description="Get a single party plan by ID",
    response_model=PartyPlan,
)
def find_party_plan(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    party_plan = db.party_plans.find_one({"id": id})
    if party_plan:
        # fetch associated invitations
        invitations = list(
            db.invitations.find({"party_plan_id": party_plan["id"]})
        )
        # return list of invitation ids
        party_plan["invitations"] = [inv["id"] for inv in invitations]

        return party_plan
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Party plan with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a party plan",
    response_model=PartyPlan,
)
def update_party_plan(
    id: UUID,
    party_plan: PartyPlanUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # get plan by id
    existing_party_plan = db.party_plans.find_one({"id": str(id)})
    if not existing_party_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with ID {id} not found",
        )

    party_plan_data = {
        k: v for k, v in party_plan.dict().items() if v is not None
    }

    # make sure searched_locations in payload are in locations database and update. this will append the searched_locations array with each update.
    if "searched_locations" in party_plan_data:
        for location_id in party_plan_data["searched_locations"]:
            if location_id not in existing_searched_locations:
                location = db.locations.find_one({"id": str(location_id)})
                if not location:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Location with ID {location_id} not found.",
                    )
                existing_searched_locations.append(location_id)

    # validate and update favorite_locations in payload. will overwrite existing list.
    if "favorite_locations" in party_plan_data:
        existing_searched_locations = existing_party_plan.get(
            "searched_locations", []
        )
        # initialize
        if party_plan_data["favorite_locations"] is None:
            party_plan_data["favorite_locations"] = []

        if not all(
            fav_id in existing_searched_locations
            for fav_id in party_plan_data["favorite_locations"]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All favorite locations must be part of searched locations.",
            )
        for fav_id in party_plan_data["favorite_locations"]:
            db.locations.update_one(
                {"id": str(fav_id)},
                {"$set": {"favorite_status": True}},
            )

    # validate that chosen_locations are part of favorite_locations. will overwrite existing list.
    if "chosen_locations" in party_plan_data:
        existing_favorite_locations = existing_party_plan.get(
            "favorite_locations", []
        )
        if not all(
            chosen_id in existing_favorite_locations
            for chosen_id in party_plan_data["chosen_locations"]
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="All chosen locations must be part of favorite locations.",
            )
        party_plan_data["chosen_locations"] = [
            chosen_id for chosen_id in party_plan_data["chosen_locations"]
        ]

    # validate invitations in payload
    if "invitations" in party_plan_data:
        invitations_to_validate = party_plan_data["invitations"]
        associated_invitations = list(
            db.invitations.find({"party_plan_id": str(id)})
        )
        associated_invitation_ids = {
            str(invitation["id"]) for invitation in associated_invitations
        }
        if not all(
            str(invitation_id) in associated_invitation_ids
            for invitation_id in invitations_to_validate
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Some provided invitation IDs are not associated with this party plan.",
            )

        # add validated invitation IDs to the party plan
        party_plan_data["invitations"] = [
            UUID(str(inv_id)) for inv_id in invitations_to_validate
        ]

    # timestamp
    current_time = datetime.now()
    party_plan_data["updated"] = current_time

    db.party_plans.update_one({"id": str(id)}, {"$set": party_plan_data})

    return db.party_plans.find_one({"id": str(id)})


@router.delete("/{id}", response_description="Delete a party plan")
def delete_party_plan(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.party_plans.delete_one({"id": id})
    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Party plan with ID {id} successfully deleted.",
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No party plan with ID {id} found. Deletion incomplete.",
    )
