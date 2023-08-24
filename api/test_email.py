from utils.email_service import send_party_invitation_email
from models.invitations import Invitation
from models.party_plans import PartyPlan
from models.locations import Location

location = Location(
    address="123 Party Street",
    city="CityName",
    state="StateName"
)

party_plan = PartyPlan(
    name="Birthday Party",
    date="25th August 2023",
    location=location
)

invitation = Invitation(
    guest_name="John Doe",
    email="jc.marti.2809@gmail.com",
    party_plan=party_plan
)

# Sample data for the test invitation
invitation = Invitation(
    account_id="dummy_account_id",
    party_id="dummy_party_id",
    guest_name="John Doe",
    party_name="Birthday Party",
    date="25th August 2023",
    location="123 Party Street",
    email="jc.marti.2809@gmail.com",  # Recipient email address
)

# Sending the test email
success = send_party_invitation_email(invitation)

# Printing the result
if success:
    print("Test email sent successfully!")
else:
    print("Failed to send the test email.")
