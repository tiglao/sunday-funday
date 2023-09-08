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


def read_html_template(file_path: str) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def fill_html_template(template_str: str, data: dict) -> str:
    for key, value in data.items():
        template_str = template_str.replace(f"{{{{ {key} }}}}", str(value))
    return template_str


def send_email(to_email, subject, content):
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
