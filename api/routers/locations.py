from json import JSONEncoder
from typing import List
from urllib import request
from uuid import UUID, uuid4

import fastapi
import requests
from clients.client import db
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from maps_api import g_key, nearby_search
from models.locations import Location, LocationUpdate
# from api.api_views import nearby_search
from party_plans import id
from utils.authenticator import authenticator

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new location",
    status_code=status.HTTP_201_CREATED,
    response_model=Location,
)
async def create_location(
    location: Location = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # check place_id error

    location = jsonable_encoder(location)
    existing_location = db.locations.find_one({"place_id": location.place_id})
    if existing_location:
        raise HTTPException(
            status_code=400,
            detail="Location with this place_id already exists",
        )

    # conversion
    # will need to add data validators later
    location_dict = jsonable_encoder(location)

    # make id
    # if not location_dict.get("id"):
    location_dict["id"] = str(uuid4())

    # add index 0 account_ids
    location_dict["account_ids"] = [location.account_id]

    print("dictionary after making new id:", location_dict)

    # add new location to database
    new_location = db.locations.insert_one(location_dict)

    # get the new location you just made from the database
    created_location = db.locations.find_one({"_id": new_location.inserted_id})
    created_location["_id"] = str(created_location["_id"])

    return created_location


@router.get(
    "/search_nearby/{location_id}",
    response_description="Search nearby locations",
)
async def search_nearby(
    location_id: str,
):
    location = db.locations.find_one({"_id": location_id})

    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found",
        )

    # Extract latitude and longitude from the location
    latitude = location.get("latitude")
    longitude = location.get("longitude")

    if latitude is None or longitude is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Latitude and/or longitude not available for this location",
        )

    # Make a request to the nearby search API
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": g_key,
        "location": f"{latitude},{longitude}",
        "radius": 1000,  # Specify the radius in meters
        "type": "restaurant",  # Adjust the type as needed
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        if results:
            for i in results:
                location["place_id"] = i["place_id"]
        return results
    else:
        return fastapi.responses.JSONResponse(
            content={"message": "Error fetching nearby places"},
            status_code=response.status_code,
        )


@router.get(
    "/",
    response_description="List all locations",
    response_model=List[Location],
)
def list_locations(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    locations = list(db.locations.find(limit=100))
    return locations


@router.get(
    "/{id}",
    response_description="Get a single location by id",
    response_model=Location,
)
def find_location(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (location := db.locations.find_one({"_id": id})) is not None:
        return location
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Location with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a location",
    response_model=LocationUpdate,
)
def update_location(
    id: UUID,
    location: LocationUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
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
    # account: dict = Depends(authenticator.get_current_account_data),
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
