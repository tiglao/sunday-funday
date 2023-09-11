from fastapi.testclient import TestClient
from main import app
from utils.email_service import send_email
from unittest.mock import patch, MagicMock

client = TestClient(app)

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
    mock_sg = mock_sg_client.return_value
    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_sg.send.return_value = mock_response

    to_email = "test@example.com"
    subject = "Test Subject"
    content = "Test Content"

    success = send_email(to_email=to_email, subject=subject, content=content)

    assert success

    mock_sg.send.assert_called_once()
