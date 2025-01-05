from unittest.mock import MagicMock, patch
import pytest
from app.services.email_service import EmailService


def test_send_email_success():
    email_service = EmailService()

    with patch("smtplib.SMTP") as MockSMTP:
        # Create a mock SMTP instance
        mock_smtp_instance = MagicMock()
        MockSMTP.return_value = mock_smtp_instance

        # Simulate successful email sending
        mock_smtp_instance.sendmail.return_value = None

        # Call the send_email method
        status_code = email_service.send_email(
            email_to="test@example.com",
            subject="Test Subject",
            body="Test Body",
            body_type="plain"
        )

        assert status_code == 200
        # mock_smtp_instance.sendmail.assert_called_once()
        # mock_smtp_instance.login.assert_called_once()
        # mock_smtp_instance.starttls.assert_called_once()
