from uuid import uuid4
from clients.client import save_invitation, get_invitation_by_id

# 1. Create a new invitation with a specific UUID
new_uuid = uuid4()
new_invitation = {
    "_id": new_uuid,
    "field1": "value1",
    "field2": "value2",
    # ... other fields
}

# Save the invitation to MongoDB
save_invitation(new_invitation)

# 2. Fetch the invitation by its UUID
fetched_invitation = get_invitation_by_id(new_uuid)

# 3. Print out the fetched invitation
print("Fetched invitation:", fetched_invitation)

# Check if the fetched invitation matches the new invitation
if fetched_invitation["_id"] == new_invitation["_id"]:
    print("The fetched invitation matches the new invitation.")
else:
    print("The fetched invitation does NOT match the new invitation.")
