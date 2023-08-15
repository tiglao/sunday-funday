from pydantic import BaseModel
from typing import List, Optional


class Invitation(BaseModel):
    account_id: str
    rsvpStatus: str


class InvitationList(BaseModel):
    invitations: List[Invitation]
