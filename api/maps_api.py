import os
import uuid
from turtle import distance
from typing import List, Optional
from dotenv import load_dotenv
import fastapi
import requests
from pydantic import BaseModel

load_dotenv()
GEOCODE_API_KEY = os.getenv("GEOCODE_API_KEY")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

def geo_code(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address}&key={GEOCODE_API_KEY}"
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


def nearby_search(location, keywords):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": SEARCH_API_KEY,
        "location": f"{location}",
        "radius": 1000,
        "keyword": keywords,
    }
    endpoint = f"{base_url}?keyword={keywords}&location={location}&radius=1500&key={SEARCH_API_KEY}"
    response = requests.get(endpoint)
    response.raise_for_status()
    if response.status_code != 200:
        raise NearbySearchError()
    data = response.json()
    if data["status"] == "OK":
        return data["results"]
  




