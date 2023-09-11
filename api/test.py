from uuid import uuid4
from clients.client import save_invitation, get_invitation_by_id

new_uuid = uuid4()
new_invitation = {
    "_id": new_uuid,
    "field1": "value1",
    "field2": "value2",
}

save_invitation(new_invitation)

fetched_invitation = get_invitation_by_id(new_uuid)

print("Fetched invitation:", fetched_invitation)

if fetched_invitation["_id"] == new_invitation["_id"]:
    print("The fetched invitation matches the new invitation.")
else:
    print("The fetched invitation does NOT match the new invitation.")
