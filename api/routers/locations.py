from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Response,
)
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID, uuid4
from utils.authenticator import authenticator
from models.locations import Location, LocationUpdate, LocationCreate
from clients.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new location",
    status_code=status.HTTP_201_CREATED,
    response_model=Location,
)
async def create_location(
    location: LocationCreate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # check for existing place_id
    existing_location = db.locations.find_one({"place_id": location.place_id})
    if existing_location:
        raise HTTPException(
            status_code=400,
            detail="Location with this place_id already exists",
        )

    # conversions and assignments
    location_dict = jsonable_encoder(location)
    location_dict["id"] = str(uuid4())
    location_dict["account_ids"] = [location.account_id]

    # add new location to database
    new_location = db.locations.insert_one(location_dict)
    created_location = db.locations.find_one({"_id": new_location.inserted_id})
    created_location["_id"] = str(created_location["_id"])

    return created_location


@router.get(
    "/",
    response_description="List all locations",
    response_description="List all locations",
    response_model=List[Location],
)
def list_locations(
    # account: dict = Depends(authenticator.get_current_account_data),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    locations = list(db.locations.find(limit=100))
    return locations
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
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (location := db.locations.find_one({"id": id})) is not None:
        return location
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Location with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a location",
    response_model=Location,
)
def update_location(
    id: UUID,
    location: LocationUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_location = db.locations.find_one({"id": str(id)})
    if not existing_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {id} not found",
        )

    location_data = {k: v for k, v in location.dict().items() if v is not None}
    if location_data:
        db.locations.update_one({"id": str(id)}, {"$set": location_data})

    return db.locations.find_one({"id": str(id)})


@router.delete("/{id}", response_description="Delete a location")
def delete_location(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.locations.delete_one({"id": id})
    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Location with ID {id}) successfully deleted.",
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No location with ID {id} found. Deletion incomplete.",
    )
