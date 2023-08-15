from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import uuid


class Test(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    test: str
    date: date
    notes: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "test": "This is a test",
                "date": "2022-02-22",
                "notes": "...",
            }
        }


class TestUpdate(BaseModel):
    test: Optional[str]
    date: Optional[date]
    notes: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "test": "This is a test",
                "date": "2022-02-22",
                "notes": "...",
            }
        }
