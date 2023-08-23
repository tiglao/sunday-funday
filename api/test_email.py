from utils.email_service import send_email, party_invitation_template

# Sample data for the test invitation
guest_name = "John Doe"
party_name = "Birthday Party"
date = "25th August 2023"
location = "123 Party Street"
rsvp_link = "https://www.example.com/rsvp"

# Creating the invitation content using the existing template
invitation_content = party_invitation_template(guest_name, party_name, date, location, rsvp_link)

# Recipient email address (replace with your email for testing)
to_email = "jc.marti.2809@gmail.com"

# Sending the test email
subject = "You're Invited to a Party!"
success = send_email(to_email, subject, invitation_content)

# Printing the result
if success:
    print("Test email sent successfully!")
else:
    print("Failed to send the test email.")
