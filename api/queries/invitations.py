from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional


class Invitation(BaseModel):


class InvitationList(BaseModel):
    invitations: List[Invitation]
