from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_party_plan():
    # Assuming you have a known party plan ID, replace "party_plan_id" with a valid ID
    party_plan_id = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/party_plans/{party_plan_id}")
    assert response.status_code == 200
    party_plan = response.json()
    assert party_plan["id"] == party_plan_id
