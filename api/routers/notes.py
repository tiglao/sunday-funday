from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Response,
    Depends,
    Request,
)
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID
from utils.authenticator import authenticator
from queries.notes import Note, NoteUpdate
from queries.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new note",
    status_code=status.HTTP_201_CREATED,
    response_model=Note,
)
async def create_note(
    note: Note = Body(...),
):
    note = jsonable_encoder(note)
    new_note = db.notes.insert_one(note)
    created_note = db.notes.find_one({"_id": new_note.inserted_id})
    created_note["_id"] = str(created_note["_id"])
    return created_note


@router.get(
    "/",
    response_description="List all notes",
    response_model=List[Note],
)
def list_notes(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    parties = list(db.notes.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single note by id",
    response_model=Note,
)
def find_note(
    id: str,
    account: dict = Depends(authenticator.get_current_account_data),
):
    if (note := db.notes.find_one({"_id": id})) is not None:
        return note
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a note",
    response_model=NoteUpdate,
)
def update_note(
    id: UUID,
    note: NoteUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_note = db.notes.find_one({"_id": str(id)})

    if not existing_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with ID {id} not found",
        )

    note_data = {k: v for k, v in note.dict().items() if v is not None}

    if note_data:
        db.notes.update_one({"_id": str(id)}, {"$set": note_data})

    return db.notes.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete a note")
def delete_note(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.notes.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note with ID {id} not found",
    )
