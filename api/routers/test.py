from fastapi import APIRouter, Body, HTTPException, status, Response
from fastapi.encoders import jsonable_encoder
from typing import List

from queries.test import Test, TestUpdate
from queries.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new test",
    status_code=status.HTTP_201_CREATED,
    response_model=Test,
)
def create_test(test: Test = Body(...)):
    test = jsonable_encoder(test)
    new_test = db.tests.insert_one(test)
    created_test = db.tests.find_one({"_id": new_test.inserted_id})
    created_test["_id"] = str(created_test["_id"])
    return created_test


@router.get(
    "/", response_description="List all tests", response_model=List[Test]
)
def list_tests():
    tests = list(db.tests.find(limit=100))
    return tests


@router.get(
    "/{id}",
    response_description="Get a single test by id",
    response_model=Test,
)
def find_test(
    id: str,
):
    if (test := db.tests.find_one({"_id": id})) is not None:
        return test
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Test with ID {id} not found",
    )


@router.put("/{id}", response_description="Update a test", response_model=Test)
def update_test(id: str, test: TestUpdate = Body(...)):
    if test.date:
        test.date = test.date.isoformat()
    test = {k: v for k, v in test.dict().items() if v is not None}
    if len(test) >= 1:
        update_result = db.tests.update_one({"_id": id}, {"$set": test})

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Test with ID {id} not found",
            )

    if (existing_test := db.tests.find_one({"_id": id})) is not None:
        return existing_test

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Test with ID {id} not found",
    )


@router.delete("/{id}", response_description="Delete a test")
def delete_test(id: str, response: Response):
    delete_result = db.tests.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Test with ID {id} not found",
    )
