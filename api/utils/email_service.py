from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import SendGridException, Mail
from models.invitations import Invitation
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import logging

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

    logging.info(f"Sending email to {to_email} with subject: {subject}")
    try:
        response = sendgrid_client.send(message)
        logging.info(f"Email sent successfully, response: {response.status_code}")
        return True  # Return True to indicate the email was sent successfully
    except SendGridException as e:
        logging.error(f"Failed to send email: {e}")
        return False  # Return False to indicate the email failed to send
