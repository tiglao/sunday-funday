import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.authenticator import authenticator
from routers import (
    party_plans,
    locations,
    invitations,
    accounts,
    emails,
)
import logging

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

app.include_router(
    party_plans.router, tags=["party plans"], prefix="/party_plans"
)
app.include_router(locations.router, tags=["locations"], prefix="/locations")
app.include_router(
    invitations.router, tags=["invitations"], prefix="/invitations"
)
app.include_router(
    locations.router, tags=["send-invitation"], prefix="/locations"
)
app.include_router(emails.router, tags=["emails"], prefix="/emails")

app.include_router(authenticator.router)
app.include_router(accounts.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
