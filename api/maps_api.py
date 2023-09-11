import fastapi
import os
import uuid
from turtle import distance
from typing import List, Optional
import requests
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")


def geo_code(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    endpoint = f"{base_url}?address={address}&key={API_KEY}"
    response = requests.get(endpoint)
    response.raise_for_status()
    results = response.json()
    if results["status"] == "OK":
        latitude = results["results"][0]["geometry"]["location"]["lat"]
        longitude = results["results"][0]["geometry"]["location"]["lng"]
        return latitude, longitude
    else:
        print(f"Geocoding failed with status: {results['status']}")


class NearbySearchError(Exception):
    pass


class PlaceError(Exception):
    pass


def nearby_search(location, keywords):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": f"{location}",
        "radius": 1000,
        "keyword": keywords,
    }
    endpoint = f"{base_url}?keyword={keywords}&location={location}&radius=1500&key={API_KEY}"
    response = requests.get(endpoint)
    response.raise_for_status()
    if response.status_code != 200:
        raise NearbySearchError()
    data = response.json()
    if data["status"] == "OK":
        return data["results"]


def get_place_info(place_id: str) -> dict:
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    print(os.environ)
    params = {"place_id": place_id, "key": API_KEY}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise PlaceError()

    return response.json()
