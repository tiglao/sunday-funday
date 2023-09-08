from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import SendGridException, Mail
from models.invitations import Invitation
from dotenv import load_dotenv
import os

load_dotenv()


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
        html_content=content)

    try:
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        return True
    except SendGridException as e:
        print("SendGrid Exception: ", e.message)
        return False
    except Exception as e:
        print("General Exception: ", e)
        return False


def send_party_invitation_email(invitation: Invitation):
    party_plan = invitation.party_plan
    subject = "You're Invited to a Party!"
    rsvp_url_accept = f'http://localhost:8000/rsvp/{invitation.id}?status=accept'
    rsvp_url_decline = f'http://localhost:8000/rsvp/{invitation.id}?status=decline'

    with open('invitation_template.html', 'r') as file:
        html = file.read()
        html = html.replace('{guest_name}', invitation.guest_name)
        html = html.replace('{party_name}', party_plan.name)
        html = html.replace('{date}', str(party_plan.date))
        html = html.replace('{location}', party_plan.location.address)
        html = html.replace('{rsvp_link_accept}', rsvp_url_accept)
        html = html.replace('{rsvp_link_decline}', rsvp_url_decline)

    send_email(email=invitation.email, subject=subject, content=html)
