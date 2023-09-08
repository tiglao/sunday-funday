# Step 1: Imports
from fastapi.testclient import TestClient
from main import app
from utils.authenticator import (
    authenticator,
)
from pydantic import BaseModel

client = TestClient(app)


class UserOut(BaseModel):
    username: str
    email: str
    roles: list[str]


def fake_get_current_account_data():
    return UserOut(
        username="testuser", email="testuser@example.com", roles=["user"]
    )


client = TestClient(app)


def test_create_account_and_get_token():
    app.dependency_overrides[
        authenticator.get_current_account_data
    ] = fake_get_current_account_data

    response = client.post(
        "/api/accounts",
        json={
            "username": "testuser@example.com",
            "password": "testpassword",
            "email": "testuser@example.com",
            "full_name": "Test User",
        },
    )

    app.dependency_overrides = {}

    assert response.status_code == 200
