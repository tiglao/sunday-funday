from json import JSONEncoder
from typing import List, Optional
from urllib import request
from uuid import UUID, uuid4

import fastapi
import pydantic
from clients.client import db
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from maps_api import NearbySearchError, nearby_search
from models.locations import Location, LocationCreate, LocationUpdate
from utils.authenticator import authenticator
from models.party_plans import PartyPlan

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new location",
    status_code=status.HTTP_201_CREATED,
    response_model=Location,
)
async def create_location(
    location: Location = Body(...),
):
    location = jsonable_encoder(location)
    existing_location = db.locations.find_one({"place_id": location.place_id})
    if existing_location:
        raise HTTPException(
            status_code=400,
            detail="Location with this place_id already exists",
        )


    new_location = db.locations.insert_one(locations)
    if not new_location.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add location to database.",
        )

    created_location = db.locations.find_one({"place_id": locations["place_id"]})
    if not created_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party plan with ID {locations['place_id']} not found after insertion.",
        )


    return created_location

@router.get(
    "/{place_id}",
    response_description="Get a single location by ID",
    response_model=Location,
)
def find_party_plan(
    place_id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    location = db.locations.find_one({"place_id": place_id})
    if location:
        # fetch associated invitations
        return location
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Location with ID {id} not found",
    )


@router.get(
    "/{party_plan_id}/search_nearby",
    response_description="Search nearby locations",
)
async def search_nearby(
    party_plan_id=str,
):
    party_plan = db.party_plans.find_one({"id": party_plan_id})
    if party_plan is not None:
        location = f'{party_plan["api_maps_location"][0]["geo"][0]},{party_plan["api_maps_location"][0]["geo"][1]}'
        keywords = party_plan["keywords"]
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Latitude and/or longitude not available for this location",
        )

    try:
        results = nearby_search(location, keywords)
        if results == None:
            print("none")
        results_dict = [{"place_id": place["place_id"]} for place in results]
    except NearbySearchError:
        return fastapi.responses.JSONResponse(
            content=jsonable_encoder({"message": "nearby search failed"}),
            status_code=400,
        )
    locations = []
    try:
        for res in results_dict:
            location = Location(**res)
            locations.append(location)
        return fastapi.responses.JSONResponse(
            content=jsonable_encoder({"locations": locations}), status_code=200
        )
    except pydantic.ValidationError as e:
        return fastapi.responses.JSONResponse(
            content=jsonable_encoder({"message": e.errors()}),
            status_code=400,
        )


@router.get(
    "/",
    response_description="List all locations",
    response_model=List[Location],
)
def list_locations():
    locations = list(db.locations.find(limit=100))
    return locations


@router.get(
    "/{place_id}",
    response_description="Get a single location by id",
    response_model=Location,
)
def find_location(
    place_id: str,
):
    if (location := db.locations.find_one({"place_id": place_id})) is not None:
        return location
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Location with ID {place_id} not found",
    )


@router.put(
    "/{place_id}",
    response_description="Update a location",
    response_model=LocationUpdate,
)
def update_location(
    place_id = str,
    location: LocationUpdate = Body(...),
):
    existing_location = db.locations.find_one({"place_id": place_id})

    if not existing_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {id} not found",
        )

    location_data = {k: v for k, v in location.dict().items() if v is not None}

    if location_data:
        db.locations.update_one({"place_id": place_id}, {"$set": location_data})

    return db.locations.find_one({"place_id": place_id})


@router.delete("/{place_id}", response_description="Delete a location location")
def delete_location(
    response: Response,
    place_id= str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.locations.delete_one({"place_id": place_id})

    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Location with id {place_id}) successfully deleted.",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No location with ID {place_id} found. Deletion incomplete.",
    )
