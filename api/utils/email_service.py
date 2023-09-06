from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import SendGridException, Mail
from models.invitations import Invitation
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(os.getenv('DATABASE_URL'))
db = client[DB_NAME]
invitations_collection = db['invitations']
accounts_collection = db['accounts']
party_plans_collection = db['party_plans']


def fetch_invitation_data(invitation_id):
    return invitations_collection.find_one({"id": invitation_id})


def fetch_account_data(account_id):
    return accounts_collection.find_one({"id": account_id})


def fetch_party_plan_data(party_plan_id):
    return party_plans_collection.find_one({"id": party_plan_id})


def send_email(to_email, subject_template, content_template, invitation_id):
    # Fetch required data
    invitation_data = fetch_invitation_data(invitation_id)
    account_data = fetch_account_data(invitation_data['account_id'])
    party_plan_data = fetch_party_plan_data(invitation_data['party_plan_id'])

    subject = subject_template.format(**invitation_data, **account_data, **party_plan_data)
    content = content_template.format(**invitation_data, **account_data, **party_plan_data)

    sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
    message = Mail(
        from_email='fundaysunday08@gmail.com',
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    print(f"Sending email to {to_email} with subject: {subject}")

    try:
        response = sendgrid_client.send(message)
        print(f"Email sent successfully, response: {response.status_code}")
    except SendGridException as e:
        print(f"Failed to send email: {e}")


def send_party_invitation_email(invitation: Invitation):
    party_plan = invitation.party_plan
    subject = "You're Invited to a Party!"

    with open('invitation_template.html', 'r') as file:
        html = file.read()
        html = html.replace('{guest_name}', invitation.guest_name)
        html = html.replace('{party_name}', party_plan.name)
        html = html.replace('{date}', str(party_plan.date))
        html = html.replace('{location}', party_plan.location.address)

    send_email(email=invitation.email, subject=subject, content=html)
