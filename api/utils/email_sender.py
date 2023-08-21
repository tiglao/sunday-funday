import os
import sys  # Import sys module to access command-line arguments
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Check if an email address argument is provided
if len(sys.argv) < 2:
    print("Usage: python send_email.py recipient@example.com")
    sys.exit(1)

recipient_email = sys.argv[1]

message = Mail(
    from_email='from@example.com',
    to_emails=recipient_email,
    subject='Sending with SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')

try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
