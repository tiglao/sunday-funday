# # in accordance with google maps policy 2023-08-24
# from pymongo import ASCENDING
# from clients.client import db


# def create_ttl_index(db):
#     db.party_plans.create_index(
#         # [("expires", 1)],
#         [("api_maps_location.geo.expires", ASCENDING)],
#         name="expires_index",
#         expireAfterSeconds=2592000,  # 30 days in seconds
#     )


# # Call the function to create the TTL index
# create_ttl_index()
