
from typing import Dict, List
from uuid import UUID, uuid4
from clients.client import db
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from models.emails import ApiEmail, EmailContext
from utils.authenticator import authenticator
from utils.invitation_vo import get_invitation

router = APIRouter()


@router.post(
    "/",
    response_description="Create a new email",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiEmail,
)
def create_email(
    invitation: Dict = Depends(get_invitation),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    # dummy account for demonstration, replace with real account data
    account = {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "fullname": "Dummy Name",
        "email": "dummy.email@example.com",
    }

    # create email context
    email_context_data = {
        "invitation_id": invitation.get("id"),
        "created_at": invitation.get("created"),
        "updated_at": invitation.get("updated"),
        "account": invitation.get("account"),
        "party_plan_id": invitation.get("party_plan_id"),
        "rsvp_status": invitation.get("rsvp_status"),
        "sent_status": "pending",  # Assuming it's pending when created
    }
    email_context = EmailContext(**email_context_data)

    # id, timestamp, account info
    email_id = str(uuid4())
    email_data = {
        "id": email_id,
        "to": f"{account['fullname']} <{account['email']}>",
        "subject": "Your Invitation",
        "template": "some_template",
        "api_context": email_context.dict(),
    }
    # add to db
    new_email = db.emails.insert_one(email_data)
    if not new_email.acknowledged:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add email to database.",
        )

    # fetch the instance you just created
    created_email = db.emails.find_one({"id": email_id})
    if not created_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email with ID {email_data['id']} not found after insertion.",
        )

    return created_email


@router.get(
    "/",
    response_description="List all emails",
    response_model=List[ApiEmail],
)
def list_emails(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    emails = list(db.emails.find(limit=100))
    return emails


@router.get(
    "/{id}",
    response_description="Get a single email by ID",
    response_model=ApiEmail,
)
def find_email(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (email := db.emails.find_one({"id": id})) is not None:
        return email
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Email with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update an email",
    response_model=ApiEmail,
)
def update_email(
    id: UUID,
    email: ApiEmail = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_email = db.emails.find_one({"id": str(id)})

    if not existing_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Email with ID {id} not found",
        )

    email_data = {k: v for k, v in email.dict().items() if v is not None}

    if email_data:
        db.emails.update_one({"id": str(id)}, {"$set": email_data})

    return db.emails.find_one({"id": str(id)})


@router.delete("/{id}", response_description="Delete an email")
def delete_email(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.emails.delete_one({"id": id})
    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Email with ID {id}) successfully deleted.",
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No email with ID {id} found. Deletion incomplete.",
    )
