from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from fastapi import (
    APIRouter,
    Body,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.encoders import jsonable_encoder
from clients.client import db
from models.notes import Note, NoteCreate, NoteUpdate
from utils.authenticator import authenticator

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new note",
    status_code=status.HTTP_201_CREATED,
    response_model=Note,
)
async def create_note(
    note: NoteCreate = Body(...),
    account: dict = Depends(authenticator.get_current_account_data),
):
    if note.party_plan_id and note.location_id:
        raise HTTPException(
            status_code=400,
            detail="A note cannot be associated with both a party plan and a location.",
        )
    if not note.party_plan_id and not note.location_id:
        raise HTTPException(
            status_code=400,
            detail="A note must be associated with either a party plan or a location.",
        )

    new_note = {
        "_id": str(uuid4()),
        "created_time": datetime.utcnow(),
        "comment": note.comment,
        "account_id": current_user,
        "party_plan_id": note.party_plan_id,
        "location_id": note.location_id,
    }

    db.notes.insert_one(new_note)

    created_note = Note(
        id=UUID(new_note["_id"]),
        created_time=new_note["created_time"],
        comment=new_note["comment"],
        account_id=new_note["account_id"],
        party_plan_id=new_note.get("party_plan_id"),
        location_id=new_note.get("location_id"),
        updated_time=None,
    )
    return created_note


@router.get(
    "/",
    response_description="List all notes",
    response_model=List[Note],
)
def list_notes():
    notes = list(db.notes.find(limit=100))
    return [{**note, "_id": str(note["_id"])} for note in notes]


@router.get(
    "/{id}",
    response_description="Get a single note by id",
    response_model=Note,
)
def find_note(
    id: str,
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

    return Note(
        id=UUID(updated_note["_id"]),
        created_time=updated_note["created_time"],
        updated_time=updated_note["updated_time"],
        comment=updated_note["comment"],
        account_id=UUID(updated_note["account_id"]),
        party_plan_id=UUID(updated_note["party_plan_id"])
        if updated_note.get("party_plan_id")
        else None,
        location_id=UUID(updated_note["location_id"])
        if updated_note.get("location_id")
        else None,
    )


@router.delete("/{id}", response_description="Delete a note")
def delete_note(
    id: str,
    response: Response,
):
    delete_result = db.notes.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Note with ID {id} not found",
    )
