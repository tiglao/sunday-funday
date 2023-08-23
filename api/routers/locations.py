from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Response,
)
from fastapi.encoders import jsonable_encoder
from typing import List
import datetime
from bson.objectid import ObjectId
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

    # add new location to database
    new_location = db.locations.insert_one(location_dict)
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
):
    updates_made = []
    removal_count = 0
    location_uuid = UUID(id)
    party_plans = list(
        db.party_plans.find(
            {
                "$or": [
                    {"searched_locations": location_uuid},
                    {"favorite_locations": location_uuid},
                    {"chosen_locations": location_uuid},
                ]
            }
        )
    )
    print("all party plans:", list(db.party_plans.find()))
    print("this locations id type:", type(id))
    print("filtered party plans:", party_plans)
    # party_plans = [
    #     {
    #         "_id": ObjectId("64e418644bb1adf01cd8e90e"),
    #         "account_id": "123456789",
    #         "general_location": "Denver, CO",
    #         "start_time": "2022-02-23T14:30:00",
    #         "end_time": "2022-02-23T17:30:00",
    #         "description": "Updated Description here ....",
    #         "image": "https://picsum.photos/201",
    #         "keywords": ["party", "drinks", "dance"],
    #         "id": UUID("f27f3102-b68a-4d9a-9c40-b4660fa3d5ea"),
    #         "created": datetime.datetime(2023, 8, 22, 2, 7, 32, 784000),
    #         "party_status": "draft",
    #         "searched_locations": [
    #             UUID("50412762-c4e4-4e2d-ab44-7aa95780e763"),
    #             UUID("6654b3d6-117b-4308-9ca2-9eb3f5dc79e0"),
    #             UUID("8e75f06f-814a-4e3a-b5cd-e8d739c946bd"),
    #             UUID("dd39e4ec-f641-4c6a-a817-7bef3ad7846e"),
    #             UUID("80ee103c-d749-4060-9e1b-069198c87d59"),
    #         ],
    #         "updated": datetime.datetime(2023, 8, 22, 14, 33, 24, 230000),
    #         "favorite_locations": [
    #             UUID("6654b3d6-117b-4308-9ca2-9eb3f5dc79e0"),
    #             UUID("dd39e4ec-f641-4c6a-a817-7bef3ad7846e"),
    #             UUID("50412762-c4e4-4e2d-ab44-7aa95780e763"),
    #             UUID("8e75f06f-814a-4e3a-b5cd-e8d739c946bd"),
    #         ],
    #         "chosen_locations": [
    #             UUID("dd39e4ec-f641-4c6a-a817-7bef3ad7846e"),
    #             UUID("50412762-c4e4-4e2d-ab44-7aa95780e763"),
    #             UUID("8e75f06f-814a-4e3a-b5cd-e8d739c946bd"),
    #         ],
    #     }
    # ]
    counts = {
        "searched_locations": 0,
        "favorite_locations": 0,
        "chosen_locations": 0,
    }
    for party_plan in party_plans:
        for new_list in counts.keys():
            if location_uuid in party_plan.get(new_list, []):
                counts[new_list] += 1
                update_result = db.party_plans.update_one(
                    {"id": party_plan["id"], new_list: location_uuid},
                    {"$pull": {new_list: location_uuid}},
                )
    for new_list, count in counts.items():
        print(f"Missing {new_list} count:", count)
    if sum(counts.values()) == 4:
        delete_result = db.locations.delete_one({"id": id})
        if delete_result.deleted_count == 1:
            return {
                "status": "success",
                "message": f"Location with ID {id} successfully deleted. Instances found: {' '.join([f'{k}: {v}' for k, v in counts.items()])}.",
            }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"No location with ID {id} found. Deletion incomplete.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Not all locations with ID {id} have been found. Deletion incomplete.",
        )
