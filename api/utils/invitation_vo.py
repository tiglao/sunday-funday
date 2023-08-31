from uuid import UUID

from clients.client import db
from fastapi import HTTPException, status


def get_invitation(invitation_id: UUID):
    associated_invitation = db.invitations.find_one({"id": str(invitation_id)})
    if not associated_invitation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No invitation found with ID {invitation_id}",
        )
    return associated_invitation
