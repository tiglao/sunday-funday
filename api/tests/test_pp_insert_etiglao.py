from fastapi.testclient import TestClient
from main import app
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

client = TestClient(app)


class ExampleDB:
    def __init__(self):
        self.db = {}

    def insert_one(self, data):
        new_id = str(uuid4())
        data["id"] = new_id
        self.db[new_id] = data
        return self

    def find_one(self, query):
        return self.db.get(query.get("id"))


example_db = ExampleDB()


class ApiMapsLocation(BaseModel):
    input: str  # Removed geo field


def test_create_party_plan():
    from clients.client import db

    app.dependency_overrides[db] = example_db

    party_plan_create_payload = {
        "account_id": "123456789",
        "api_maps_location": [{"input": "New York, NY"}],
        "start_time": "2022-02-23T14:30:00",
        "end_time": "2022-02-23T17:30:00",
        "description": "Updated Description here ....",
        "keywords": ["party", "drinks", "dance"],
    }

    response = client.post("/party_plans", json=party_plan_create_payload)

    app.dependency_overrides = {}

    assert response.status_code == 201

    created_party_plan = response.json()

    assert created_party_plan["account_id"] == "123456789"
    assert created_party_plan["start_time"] == "2022-02-23T14:30:00"
    assert created_party_plan["end_time"] == "2022-02-23T17:30:00"
    assert created_party_plan["description"] == "Updated Description here ...."
    assert created_party_plan["keywords"] == ["party", "drinks", "dance"]

    assert "id" in created_party_plan
    assert "created" in created_party_plan
    assert created_party_plan["party_status"] == "draft"
