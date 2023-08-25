from fastapi.testclient import TestClient
from main import app
from utils.email_service import send_email
from unittest.mock import patch, MagicMock

client = TestClient(app)

# Example test data - adjust as needed
test_email_data = {
    "to": "jc.marti.2809@gmail.com",
    "subject": "Party Invitation",
    "template": "invitation_template.html",
    "context": {
        "name": "John",
        "party_theme": "Halloween",
    },
}


@patch("utils.email_service.SendGridAPIClient")
def test_send_email(mock_sg_client):
    # Configure the mock SendGrid client to simulate a successful response
    mock_sg = mock_sg_client.return_value
    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_sg.send.return_value = mock_response

    # Define the test email parameters
    to_email = "test@example.com"
    subject = "Test Subject"
    content = "Test Content"

    # Call the send_email function with the test data
    success = send_email(to_email=to_email, subject=subject, content=content)

    # Check that the function returned True, indicating success
    assert success

    # Check that the SendGrid send method was called exactly once
    mock_sg.send.assert_called_once()


def test_actual_email():
    to_email = 'jc.marti.2809@gmail.com'
    subject = 'Test Email'
    content = '<h1>This is a test email</h1>'

    success = send_email(to_email, subject, content)

    if success:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")


if __name__ == "__main__":
    test_actual_email()
