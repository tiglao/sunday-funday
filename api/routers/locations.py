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
from models.locations import Location, LocationUpdate
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

    location_dict = jsonable_encoder(location)

    location_dict["id"] = str(uuid4())

    location_dict["account_ids"] = [location.account_id]

    print("dictionary after making new id:", location_dict)

    new_location = db.locations.insert_one(location_dict)

    created_location = db.locations.find_one({"_id": new_location.inserted_id})
    created_location["_id"] = str(created_location["_id"])

    return created_location


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
        print(location)
        print(keywords)
        print(party_plan)
        print(party_plan_id)
    if location is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Latitude and/or longitude not available for this location",
        )

    try:
        results = nearby_search(location, keywords)
        print(results)
        if results == None:
            print("none")
        results_dict = [{"place_id": place["place_id"]} for place in results]
        print(results_dict)
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
    "/{id}",
    response_description="Update a location",
    response_model=LocationUpdate,
)
def update_location(
    id: UUID,
    location: LocationUpdate = Body(...),
):
    existing_location = db.locations.find_one({"_id": str(id)})

    if not existing_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {id} not found",
        )

    location_data = {k: v for k, v in location.dict().items() if v is not None}

    if location_data:
        db.locations.update_one({"_id": str(id)}, {"$set": location_data})

    return db.locations.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete a location location")
def delete_location(
    id: str,
    response: Response,
):
    delete_result = db.locations.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Location with id {id}) successfully deleted.",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No location with ID {id} found. Deletion incomplete.",
    )
