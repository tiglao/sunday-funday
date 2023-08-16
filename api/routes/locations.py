from fastapi import APIRouter, Body, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID

from queries.locations import Location, LocationUpdate
from queries.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new location",
    status_code=status.HTTP_201_CREATED,
    response_model=Location,
)
def create_location(plan: Location = Body(...)):
    plan = jsonable_encoder(plan)
    new_location = db.locations.insert_one(plan)
    created_location = db.locations.find_one({"_id": new_location.inserted_id})
    created_location["_id"] = str(created_location["_id"])
    return created_location


@router.get(
    "/",
    response_description="List all parties",
    response_model=List[Location],
)
def list_locations():
    parties = list(db.locations.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single location by id",
    response_model=Location,
)
def find_location(
    id: str,
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
def update_location(id: UUID, location: LocationUpdate = Body(...)):
    existing_location = db.locations.find_one({"_id": str(id)})

    if not existing_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {id} not found",
        )

    if location.startTime:
        location.date = location.date.isoformat()

    location_data = {k: v for k, v in location.dict().items() if v is not None}

    if location_data:
        db.locations.update_one({"_id": str(id)}, {"$set": location_data})

    return db.locations.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete a location plan")
def delete_location(id: str, response: Response):
    delete_result = db.locations.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Location with ID {id} not found",
    )
