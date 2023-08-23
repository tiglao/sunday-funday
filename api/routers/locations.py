from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Response,
    Depends,
)
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID
from utils.authenticator import authenticator
from models.locations import Location, LocationUpdate
from clients.client import db
from api_views import nearby_search
from party_plans import id



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
    party_plan_id = party_plan["id"]
    nearby_search = nearby_search()
    try:
        search_result = nearby_search(location.address, nearby_search.key, nearby_search.keyword)
        if search_result is None:
            return Error(message="Places API Issue")
            
        location = search_result 
    existing_location = db.locations.find_one({"place_id": location.place_id})
    if existing_location:
        raise HTTPException(
            status_code=400,
            detail="Location with this place_id already exists")

    # conversion
    # will need to add data validators later
    location_dict = jsonable_encoder(location)

    # make id
    # if not location_dict.get("id"):
    location_dict["id"] = str(uuid4())

    #add index 0 account_ids
    location_dict["account_ids"] = [location.account_id]

    print("dictionary after making new id:", location_dict)

    # add new location to database
    new_location = db.locations.insert_one(location_dict)

    # get the new location you just made from the database
    created_location = db.locations.find_one({"_id": new_location.inserted_id})
    created_location["_id"] = str(created_location["_id"])

    return created_location


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
