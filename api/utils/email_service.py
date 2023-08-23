from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import SendGridException, Mail
import os


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


def party_invitation_template(
    guest_name,
    party_name, date,
    location,
    rsvp_link,
):
    with open('invitation_template.html', 'r') as file:
        html_content = file.read().format(
            guest_name=guest_name,
            party_name=party_name,
            date=date,
            location=location,
            rsvp_link=rsvp_link
        )
    return html_content
