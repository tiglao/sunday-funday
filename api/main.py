import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes import party_plan, locations, invitations

app = FastAPI()
app.include_router(
    party_plan.router, tags=["party_plan"], prefix="/party_plan"
)
app.include_router(locations.router, tags=["locations"], prefix="/locations")
app.include_router(
    invitations.router, tags=["invitations"], prefix="/invitations"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
