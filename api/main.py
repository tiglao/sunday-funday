from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from routes import test

app = FastAPI()
app.include_router(test.router, tags=["tests"], prefix="/test")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
