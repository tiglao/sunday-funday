from fastapi.testclient import TestClient
from main import app
from models.party_plans import PartyPlan
import json
from pydantic import BaseModel

client = TestClient(app)


def test_create_party_plan_with_geocode():
    party_plan_data = {
        "account_id": "123456789",
        "description": "Test party",
        "api_maps_location": [
            {
                "input": "Berlin"
            }
        ],
        "start_time": "2023-08-25T18:00:00",
        "end_time": "2023-08-25T22:00:00",
        "image": "https://static.wikia.nocookie.net/p__/images/2/2a/Deyfm3s-62419a2b-95be-4ab4-81f8-8c37ba6b0091.png/revision/latest/thumbnail/width/360/height/360?cb=20220825190009&path-prefix=protagonist",
        "keywords": ["Drinks", "Dinner"]
    }

    response = client.post('/party_plans/', json=party_plan_data)

    assert response.status_code == 201

    created_party_plan = response.json()

    assert 'geo' in created_party_plan['api_maps_location'][0]

def test_search_nearby():
    party_plan_data = {
        "account_id": "123456789",
        "description": "Test party",
        "api_maps_location": [
            {
                "input": "Berlin"
            }
        ],
        "start_time": "2023-08-25T18:00:00",
        "end_time": "2023-08-25T22:00:00",
        "image": "https://static.wikia.nocookie.net/p__/images/2/2a/Deyfm3s-62419a2b-95be-4ab4-81f8-8c37ba6b0091.png/revision/latest/thumbnail/width/360/height/360?cb=20220825190009&path-prefix=protagonist",
        "keywords": ["Drinks", "Dinner"]
    }
    response = client.post('/party_plans/', json=party_plan_data)

    assert response.status_code == 201

    response_json = response.json()

    id = response_json.get('id')

    response = client.get('/locations/{id}/search_nearby')

    assert response.status_code == 200

    assert response != None
