import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import accounts, invitations, locations, party_plans
from utils.authenticator import authenticator

# from routers import accounts

app = FastAPI()
app.include_router(
    party_plans.router, tags=["party plans"], prefix="/party_plans"
)
app.include_router(locations.router, tags=["locations"], prefix="/locations")
app.include_router(
    invitations.router, tags=["invitations"], prefix="/invitations"
)
app.include_router(notes.router, tags=["notes"], prefix="/notes")

app.include_router(authenticator.router)
# app.include_router(accounts.router, tags=["accounts"], prefix="/accounts")
app.include_router(accounts.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
