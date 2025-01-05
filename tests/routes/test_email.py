from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.services.email_service import EmailService
from app.dependencies.injection import get_email_service
from app.schemas.email import EmailIn

# Mock EmailService for dependency injection
@pytest.fixture
def mock_email_service():
    mock_service = MagicMock(spec=EmailService)
    return mock_service

# Dependency override for FastAPI
@pytest.fixture
def client(mock_email_service):
    app.dependency_overrides[get_email_service] = lambda: mock_email_service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_email_callback_success(client, mock_email_service):
    # Mock the send_email method to return 200
    mock_email_service.send_email.return_value = 200

    # Prepare test data
    test_data = {
        "subject": "Test Subject",
        "body": "Test Body",
        "msg_type": "plain"
    }

    response = client.post("/email/", json=test_data)

    # Assertions
    assert response.status_code == 200


def test_email_callback_failure(client, mock_email_service):
    # Mock the send_email method to return an error status code
    mock_email_service.send_email.return_value = 500

    # Prepare test data
    test_data = {
        "subject": "Test Subject",
        "body": "Test Body",
        "msg_type": "plain"
    }

    response = client.post("/email/", json=test_data)

    # Assertions
    assert response.status_code == 500
