import os
import uuid
from turtle import distance
from typing import List, Optional

import fastapi
import requests
from api_keys import API_KEY
from pydantic import BaseModel


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


def nearby_search(location, keywords):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": f"{location}",
        "radius": 1000,
        "keyword": keywords,
    }
    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise NearbySearchError()

    data = response.json()
    results = data.get("results", [])
    return results


class Places(BaseModel):
    def setUp(self):
        address_components = Optional[List[str]]
        adr_address = Optional[str]
        fomatted_phone_number = Optional[str]
        icon = Optional[str]
        place_id = str
        rating = Optional[int]
        types = Optional[List[str]]
        website = Optional[str]
        self.location = [str]
        self.radius = 100
        review = [List[PlaceReview]]  # should be a foreign key
        PlaceReview = {
            "author_name": "John_Smith",
            "rating": "2",
            "relative_time_description": "2000-01-01T00:00:00",
            "time": "2000-01-01T00:00:00",  # use DateTimeField
        }

    def nearby_search(api_key, location, keyword=None, radius=None, type=None):
        base_url = (
            "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        )

        params = {
            "key": api_key,
            "location": location.latitude + location.longitude,
            "radius": radius,
            "keyword": keyword,
            "type": type,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            results = data["results"]
            return results
        else:
            error_message = data.get("error_message", "Unknown error")
            raise Exception(f"API request failed: {error_message}")

    if __name__ == "__main__":
        api_key = "AIzaSyA-5Jr7-9Q53rLg1lTZc-vj1VOgRAHoHw8"
        location = "-33.86746,151.20709"
        latitude = "-33.86746"
        longitude = "151.20709"
        keyword = "restaurant"
        radius = 1000  # Radius in meters
        place_type = "restaurant"

        results = nearby_search(api_key, location, keyword, radius, place_type)

        for result in results:
            name = result.get("name", "Unnamed Place")
            address = result.get("vicinity", "No address available")
            print(f"Name: {name}")
            print(f"Address: {address}")
            print("-" * 20)
