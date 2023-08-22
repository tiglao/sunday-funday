from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import os


load_dotenv()


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
    except Exception as e:
        print(e)


def party_invitation_template(
    guest_name,
    party_name,
    date,
    location,
    rsvp_link,
):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f3f3f3;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
            }}
            .header {{
                font-size: 24px;
                text-align: center;
                color: #E91E63;
            }}
            .content {{
                margin: 20px 0;
            }}
            .button {{
                display: block;
                text-align: center;
                background-color: #4CAF50;
                padding: 14px 20px;
                text-decoration: none;
                color: white;
                border-radius: 4px;
                margin: 10px auto;
                width: 200px;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">You're Invited!</div>
            <div class="content">
                <p>Hello {guest_name},</p>
                <p>You are invited to {party_name} on {date} at {location}.</p>
                <a href="{rsvp_link}" class="button">RSVP Now</a>
            </div>
            <div class="footer">See you there!</div>
        </div>
    </body>
    </html>
    """
