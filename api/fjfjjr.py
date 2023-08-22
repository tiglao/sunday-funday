lets start with models:

accounts.py

from pydantic import BaseModel
from jwtdown_fastapi.authentication import Token


class LogOut(BaseModel):
    account_id: str


class LogIn(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class Account(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str
    avatar: str
    user_name: str
    id: str


class AccountUpdate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    date_of_birth: str
    avatar: str


class DuplicateAccountError(ValueError):
    pass


class AccountIn(BaseModel):
    username: str
    password: str
    full_name: str


class AccountOut(BaseModel):
    id: str
    username: str
    full_name: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountForm(BaseModel):
    username: str
    password: str


class AccountToken(Token):
    account: AccountOut
    # pass

apis.py

from pydantic import BaseModel


class HttpError(BaseModel):
    detail: str

invitations.py

from pydantic import BaseModel, Field
from typing import Optional
import uuid


class Invitation(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    account_id: str
    rsvpStatus: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "account_id": "76565765",
            }
        }


class InvitationUpdate(BaseModel):
    account_id: Optional[str]
    rsvpStatus: Optional[bool]

    class Config:
        schema_extra = {
            "example": {"account_id": "76565765", "rsvpStatus": "False"}
        }

locations.py

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict
import uuid


class Location(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    place_id: str
    name: str
    address: str
    type: str
    category: str
    favorite_status: bool = False
    notes: Optional[str]
    hours_of_operation: Optional[Dict[str, str]]
    website: Optional[HttpUrl]
    image: Optional[HttpUrl]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "place_id": "76565765",
                "name": "Drink and Drown",
                "address": "1234 street",
                "type": "?????",
                "category": "Bars",
                "notes": "...",
                "hoursOfOperation": {
                    "Monday": "9am - 8pm",
                    "Tuesday": "9am - 8pm",
                    "Wednesday": "9am - 8pm",
                    "Thursday": "9am - 8pm",
                    "Friday": "9am - 8pm",
                    "Saturday": "9am - 8pm",
                },
                "website": "https://www.google.com",
                "image": "https://picsum.photos/200",
            }
        }


class LocationUpdate(BaseModel):
    place_id: Optional[str]
    name: Optional[str]
    address: Optional[str]
    lat: Optional[float]
    lon: Optional[float]
    type: Optional[str]
    category: Optional[str]
    favoriteStatus: Optional[bool]
    notes: Optional[str]
    hoursOfOperation: Optional[dict]
    website: Optional[HttpUrl]
    image: Optional[HttpUrl]

    class Config:
        schema_extra = {
            "example": {
                "place_id": "76565765",
                "name": "Drink and Drown",
                "address": "1234 street",
                "lat": "12242",
                "lon": "17043",
                "type": "?????",
                "category": "Bars",
                "notes": "...",
                "hoursOfOperation": {
                    "Monday": "9am - 8pm",
                    "Tuesday": "9am - 8pm",
                    "Wednesday": "9am - 8pm",
                    "Thursday": "9am - 8pm",
                    "Friday": "9am - 8pm",
                    "Saturday": "9am - 8pm",
                },
                "website": "https://www.google.com",
                "image": "https://picsum.photos/200",
            }
        }


# class Location(BaseModel):
#     place_id: str
#     name: str
#     address: str
#     lat: float
#     lon: float
#     type: str ????
#     category: str
#     favoriteStatus: Optional[bool] = Field(None, description = "empty until selection process. all not favorited = False")
#     notes: Optional[str] = Field(None, description = "collection of multiple comments about the location")
#     hoursOfOperation: Optional[dict] = Field(None, description="dictionary with days as keys")
#     website: Optional[HttpUrl]
#     image: Optional[HttpUrl]

# class LocationList(BaseModel):
#     locations: List[Location]


party_plans.py

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, List
from datetime import date, datetime
import uuid


class PartyPlan(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    username: str
    notes: str
    date: date
    invitations: Optional[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    party_status: str
    keywords: List[str]
    general_location: str
    favorite_locations: Optional[Dict[str, str]]
    description: str
    image: Optional[HttpUrl]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "username": "Billy1234",
                "notes": "Notes go here....",
                "date": "2022-02-22",
                "invitees": {
                    "name": "id",
                    "name": "id",
                    "name": "id",
                    "name": "id",
                },
                "start_time": "2022-02-22 14:30",
                "end_time": "2022-02-22 17:30",
                "party_status": "draft",
                "keywords": ["fun", "bar", "burgers"],
                "general_location": "Denver",
                "favorite_locations": {
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                },
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
            }
        }


class PartyPlanUpdate(BaseModel):
    username: Optional[str]
    notes: Optional[str]
    date: Optional[date]
    invitations: Optional[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    party_status: Optional[str]
    keywords: Optional[List[str]]
    general_location: Optional[str]
    favorite_locations: Optional[Dict[str, str]]
    chosen_locations: Optional[Dict[str, str]]
    description: Optional[str]
    image: Optional[HttpUrl]

    class Config:
        schema_extra = {
            "example": {
                "id": "generated",
                "username": "Billy1234",
                "notes": "Notes go here....",
                "date": "2022-02-22",
                "invitees": {
                    "name": "id",
                    "name": "id",
                    "name": "id",
                    "name": "id",
                },
                "start_time": "2022-02-22 14:30",
                "end_time": "2022-02-22 17:30",
                "party_status": "draft",
                "keywords": ["fun", "bar", "burgers"],
                "general_location": "Denver",
                "favorite_locations": {
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                    "location name": "place_id",
                },
                "description": "Description here ....",
                "image": "https://picsum.photos/200",
            }
        }

repositories folder:

accounts.py

from pydantic import BaseModel
from clients.client import db
from models.accounts import (
    AccountOutWithPassword,
    AccountIn,
    DuplicateAccountError,
)

collection = db["accounts"]


class AccountRepo(BaseModel):
    def get(self, username: str) -> AccountOutWithPassword:
        acc = collection.find_one({"username": username})
        print
        if not acc:
            return None
        acc["id"] = str(acc["_id"])
        return AccountOutWithPassword(**acc)

    def create(
        self, info: AccountIn, hashed_password: str
    ) -> AccountOutWithPassword:
        info = info.dict()
        if self.get(info["username"]) is not None:
            raise DuplicateAccountError
        info["hashed_password"] = hashed_password
        del info["password"]
        collection.insert_one(info)
        id = str(info["_id"])
        acc = AccountOutWithPassword(**info, id=id)
        return acc

routers folder:

accounts.py

from fastapi import (
    Depends,
    HTTPException,
    status,
    Response,
    APIRouter,
    Request,
)

from utils.authenticator import authenticator
from models.accounts import (
    AccountIn,
    AccountOut,
    AccountForm,
    AccountToken,
    DuplicateAccountError,
)
from models.apis import HttpError
from repositories.accounts import AccountRepo


router = APIRouter()


# @router.get("/token", response_model=AccountToken)
# async def get_token(request: Request) -> AccountToken:
#     # check for cookie
#     if authenticator.cookie_name not in request.cookies:
#         raise HTTPException(
#             status_code=400, detail="Required cookie not found"
#         )

#     # response body
#     return {
#         "access_token": request.cookies[authenticator.cookie_name],
#         "type": "Bearer",
#     }


@router.get("/token", response_model=AccountToken | None)
async def get_token(
    request: Request,
    account: AccountOut = Depends(authenticator.try_get_current_account_data),
) -> AccountToken | None:
    if account and authenticator.cookie_name in request.cookies:
        return {
            "access_token": request.cookies[authenticator.cookie_name],
            "type": "Bearer",
            "account": account,
        }


# AUTH clause. Use this function when ready
# @router.get("/token", response_model=AccountToken | None)
# async def get_token(
#     request: Request,
#     account: AccountOut = Depends(authenticator.try_get_current_account_data),
# ) -> AccountToken | None:
#     print("request is:", request)
#     if not account:
#          raise HTTPException(status_code=404, detail="Account not found")
#     elif authenticator.cookie_name not in request.cookies:
#         raise HTTPException(
#             status_code=400, detail="Required cookie not found"
#         )
#     elif authenticator.cookie_name in request.cookies:
#         return {
#             "access_token": request.cookies[authenticator.cookie_name],
#             "type": "Bearer",
#         }


@router.post("/api/accounts", response_model=AccountToken | HttpError)
async def create_account(
    info: AccountIn,
    request: Request,
    response: Response,
    repo: AccountRepo = Depends(),
):
    hashed_password = authenticator.hash_password(info.password)
    try:
        account = repo.create(info, hashed_password)
    except DuplicateAccountError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create an account with those credentials",
        )
    form = AccountForm(username=info.username, password=info.password)
    token = await authenticator.login(response, request, form, repo)
    return AccountToken(account=account, **token.dict())

invitations.py

from fastapi import APIRouter, Body, HTTPException, status, Response, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID
from utils.authenticator import authenticator
from models.invitations import Invitation, InvitationUpdate
from clients.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new invitation",
    status_code=status.HTTP_201_CREATED,
    response_model=Invitation,
)
def create_invitation(
    plan: Invitation = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    plan = jsonable_encoder(plan)
    new_invitation = db.invitations.insert_one(plan)
    created_invitation = db.invitations.find_one(
        {"_id": new_invitation.inserted_id}
    )
    created_invitation["_id"] = str(created_invitation["_id"])
    return created_invitation


@router.get(
    "/",
    response_description="List all invitations",
    response_model=List[Invitation],
)
def list_invitations(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    invitations = list(db.invitations.find(limit=100))
    return invitations


@router.get(
    "/{id}",
    response_description="Get a single invitation by ID",
    response_model=Invitation,
)
def find_invitation(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (invitation := db.invitations.find_one({"_id": id})) is not None:
        return invitation
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invitation with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update an invitation",
    response_model=InvitationUpdate,
)
def update_invitation(
    id: UUID,
    invitation: InvitationUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_invitation = db.invitations.find_one({"_id": str(id)})

    if not existing_invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invitation with ID {id} not found",
        )

    invitation_data = {
        k: v for k, v in invitation.dict().items() if v is not None
    }

    if invitation_data:
        db.invitations.update_one({"_id": str(id)}, {"$set": invitation_data})

    return db.invitations.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete an invitation")
def delete_invitation(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.invitations.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Invitation with id {id}) successfully deleted.",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No invitation with ID {id} found. Deletion incomplete.",
    )

locations.py

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


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new location",
    status_code=status.HTTP_201_CREATED,
    response_model=Location,
)
async def create_location(
    plan: Location = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    plan = jsonable_encoder(plan)
    new_location = db.locations.insert_one(plan)
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


@router.delete("/{id}", response_description="Delete a location plan")
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


party_plans.py

from fastapi import APIRouter, Body, HTTPException, status, Response, Depends
from fastapi.encoders import jsonable_encoder
from typing import List
from uuid import UUID
from utils.authenticator import authenticator
from models.party_plans import PartyPlan, PartyPlanUpdate
from clients.client import db


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new party plan",
    status_code=status.HTTP_201_CREATED,
    response_model=PartyPlan,
)
def create_party_plan(
    plan: PartyPlan = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    plan = jsonable_encoder(plan)
    new_plan = db.party_plan.insert_one(plan)
    created_plan = db.party_plan.find_one({"_id": new_plan.inserted_id})
    created_plan["_id"] = str(created_plan["_id"])
    return created_plan


@router.get(
    "/",
    response_description="List all party plans",
    response_model=List[PartyPlan],
)
def list_party_plans(
    # account: dict = Depends(authenticator.get_current_account_data),
):
    parties = list(db.party_plan.find(limit=100))
    return parties


@router.get(
    "/{id}",
    response_description="Get a single party plan by ID",
    response_model=PartyPlan,
)
def find_party_plan(
    id: str,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    if (party := db.party_plan.find_one({"_id": id})) is not None:
        return party
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Party with ID {id} not found",
    )


@router.put(
    "/{id}",
    response_description="Update a party plan",
    response_model=PartyPlanUpdate,
)
def update_party_plan(
    id: UUID,
    party: PartyPlanUpdate = Body(...),
    # account: dict = Depends(authenticator.get_current_account_data),
):
    existing_party = db.party_plan.find_one({"_id": str(id)})

    if not existing_party:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Party with ID {id} not found",
        )

    if party.start_time:
        party.date = party.date.isoformat()

    party_data = {k: v for k, v in party.dict().items() if v is not None}

    if party_data:
        db.party_plan.update_one({"_id": str(id)}, {"$set": party_data})

    return db.party_plan.find_one({"_id": str(id)})


@router.delete("/{id}", response_description="Delete a party plan")
def delete_party_plan(
    id: str,
    response: Response,
    # account: dict = Depends(authenticator.get_current_account_data),
):
    delete_result = db.party_plan.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return {
            "status": "success",
            "message": f"Party plan with id {id}) successfully deleted.",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No party plan with ID {id} found. Deletion incomplete.",
    )

rm_accounts.py

from pydantic import BaseModel
from queries.client import db

collection = db["accounts"]


class DuplicateAccountError(ValueError):
    pass


class AccountIn(BaseModel):
    username: str
    password: str
    full_name: str


class AccountOut(BaseModel):
    id: str
    username: str
    full_name: str


class AccountOutWithPassword(AccountOut):
    hashed_password: str


class AccountRepo(BaseModel):
    def get(self, username: str) -> AccountOutWithPassword:
        acc = collection.find_one({"username": username})
        print
        if not acc:
            return None
        acc["id"] = str(acc["_id"])
        return AccountOutWithPassword(**acc)

    def create(
        self, info: AccountIn, hashed_password: str
    ) -> AccountOutWithPassword:
        info = info.dict()
        if self.get(info["username"]) is not None:
            raise DuplicateAccountError
        info["hashed_password"] = hashed_password
        del info["password"]
        collection.insert_one(info)
        id = str(info["_id"])
        acc = AccountOutWithPassword(**info, id=id)
        return acc


# class LogOut(BaseModel):
#     account_id: str


# class LogIn(BaseModel):
#     email: str
#     password: str
#     first_name: str
#     last_name: str


# class Account(BaseModel):
#     email: str
#     password: str
#     first_name: str
#     last_name: str
#     date_of_birth: str
#     avatar: str
#     user_name: str
#     id:str


# class AccountUpdate(BaseModel):
#     email: str
#     password: str
#     first_name: str
#     last_name: str
#     date_of_birth: str
#     avatar: str

utils folder:

authenticator.py

import os
from fastapi import Depends
from jwtdown_fastapi.authentication import Authenticator
from models.accounts import AccountOut, AccountOutWithPassword
from repositories.accounts import AccountRepo


class MyAuthenticator(Authenticator):
    async def get_account_data(
        self,
        username: str,
        accounts: AccountRepo,
    ):
        # Use your repo to get the account based on the
        # username (which could be an email)
        return accounts.get(username)

    def get_account_getter(
        self,
        accounts: AccountRepo = Depends(),
    ):
        # Return the accounts. That's it.
        return accounts

    def get_hashed_password(self, account: AccountOutWithPassword):
        # Return the encrypted password value from your
        # account object
        return account.hashed_password

    def get_account_data_for_cookie(self, account: AccountOut):
        # Return the username and the data for the cookie.
        # You must return TWO values from this method.
        return account.username, AccountOut(**account.dict())


authenticator = MyAuthenticator(os.environ["SIGNING_KEY"])

email_service.py

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os


def send_email(to_email, subject, content):
    sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    message = Mail(
        from_email='fundaysunday08@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=content)

    try:
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
    except Exception as e:
        print(e)


def party_invitation_template(guest_name, party_name, date, location, rsvp_link):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f3f3f3;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
            }}
            .header {{
                font-size: 24px;
                text-align: center;
                color: #E91E63;
            }}
            .content {{
                margin: 20px 0;
            }}
            .button {{
                display: block;
                text-align: center;
                background-color: #4CAF50;
                padding: 14px 20px;
                text-decoration: none;
                color: white;
                border-radius: 4px;
                margin: 10px auto;
                width: 200px;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">You're Invited!</div>
            <div class="content">
                <p>Hello {guest_name},</p>
                <p>You are invited to {party_name} on {date} at {location}.</p>
                <a href="{rsvp_link}" class="button">RSVP Now</a>
            </div>
            <div class="footer">See you there!</div>
        </div>
    </body>
    </html>
    """

all of these folders are within the api folder and what follows are the other files within the api folder:

main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.authenticator import authenticator
from routers import (
    party_plans,
    locations,
    invitations,
    accounts,
)

app = FastAPI()


app.include_router(
    party_plans.router, tags=["party plans"], prefix="/party_plans"
)
app.include_router(locations.router, tags=["locations"], prefix="/locations")
app.include_router(
    invitations.router, tags=["invitations"], prefix="/invitations"
)
app.include_router(authenticator.router)
app.include_router(accounts.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

requirements.txt

fastapi[all]==0.91.0
uvicorn[standard]==0.17.6
pymongo==4.4.1
jwtdown-fastapi>=0.5.0
pytest


Dockerfile

FROM python:3.10-bullseye
RUN python -m pip install --upgrade pip
WORKDIR /app

# Copy the top-level files in your service's directory
# Modify these instructions to do that
COPY requirements.txt requirements.txt
COPY main.py main.py

# Copy all of the subdirectories in your service's directory
# Modify these instructions to do that
# COPY queries queries
# COPY routers routers

RUN python -m pip install -r requirements.txt

# !! PORT env var needs to match with exposed port in caprover dashboard
CMD uvicorn main:app --host 0.0.0.0 --port 80


# If you're using a relational database and want migrations
# to be run automatically, delete the previous CMD line and
# uncomment the following COPY and CMD lines
# COPY migrations migrations
# # !! PORT env var needs to match with exposed port in caprover dashboard
# CMD python -m migrations up && uvicorn main:app --host 0.0.0.0 --port 80

Dockerfile.dev

FROM python:3.10-bullseye
RUN python -m pip install --upgrade pip
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
WORKDIR /deps
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
WORKDIR /app
CMD /wait && uvicorn main:app --reload --host 0.0.0.0

# If you're using a relational database and want migrations
# to be run automatically, delete the previous CMD line and
# uncomment this CMD line
# CMD /wait && python -m migrations up && uvicorn main:app --reload --host 0.0.0.0

outside of the api folder, in the root directory:

docker-compose.yaml

volumes:
  sunday_funday:
    external: true

services:
  fastapi:
    environment:
      CORS_HOST: http://localhost:3000
      DATABASE_URL: mongodb://root:example@mongo
      DB_NAME: sunday_funday
      SIGNING_KEY: ${SIGNING_KEY}
    build:
      context: api
      dockerfile: Dockerfile.dev
    ports:
      - 8000:8000
    volumes:
      - ./api:/app
    working_dir: /app
    depends_on:
      - mongo

  mongo:
    image: mongo
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - sunday_funday:/data/db

  mongo-express:
    image: mongo-express
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: example
      ME_CONFIG_MONGODB_SERVER: mongo
    ports:
      - "8081:8081"
    depends_on:
      - mongo
    restart: always

  ghi:
    image: node:lts-bullseye
    command: /bin/bash run.sh
    working_dir: /app
    volumes:
      - ./ghi:/app
    ports:
      - "3000:3000"
    environment:
      HOST_OS: ${OS}
      NODE_ENV: development
      HOST: "0.0.0.0"
      PUBLIC_URL: http://localhost:3000
      REACT_APP_API_HOST: ${REACT_APP_API_HOST}

  sendmail:
    image: pigeosolutions/docker-sendmail
    environment:
      - HOSTNAME=my-sendmail-container
      - WHITELIST_FROM=fundaysunday08@gmail.com
