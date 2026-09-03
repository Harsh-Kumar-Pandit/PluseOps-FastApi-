import pytest
from unittest.mock import patch
from app.models import User, Monitor, Notification, Incident
from app.workers.tasks import send_notification_email_task
from app.core.security import hash_password
from datetime import datetime
import app.services.email

@pytest.fixture
def email_test_data(db_session):
    user = User(
        name="Email Test User",
        email="email_test@example.com",
        password=hash_password("password123"),
        email_notifications_enabled=True,
        down_alerts_enabled=True,
        recovery_alerts_enabled=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    monitor = Monitor(
        user_id=user.id,
        name="Email Test Monitor",
        url="http://example.com",
        is_active=True,
        method="GET",
        expected_status=200
    )
    db_session.add(monitor)
    db_session.commit()
    db_session.refresh(monitor)

    incident = Incident(
        monitor_id=monitor.id,
        status="OPEN",
        reason="Test Reason",
        started_at=datetime.utcnow()
    )
    db_session.add(incident)
    db_session.commit()
    db_session.refresh(incident)

    notif_down = Notification(
        user_id=user.id,
        monitor_id=monitor.id,
        incident_id=incident.id,
        type="DOWN",
        title="Down Alert",
        message="DOWN message",
        created_at=datetime.utcnow()
    )
    notif_recovery = Notification(
        user_id=user.id,
        monitor_id=monitor.id,
        incident_id=incident.id,
        type="RECOVERY",
        title="Recovery Alert",
        message="RECOVERY message",
        created_at=datetime.utcnow()
    )
    db_session.add_all([notif_down, notif_recovery])
    db_session.commit()
    db_session.refresh(notif_down)
    db_session.refresh(notif_recovery)

    return {
        "user": user,
        "monitor": monitor,
        "incident": incident,
        "notif_down": notif_down,
        "notif_recovery": notif_recovery
    }

@patch("app.services.email.RESEND_API_KEY", "test_key")
@patch("app.services.email.resend.Emails.send")
def test_down_email_sent(mock_resend, email_test_data, db_session):
    mock_resend.return_value = {"id": "resend_id_123"}
    send_notification_email_task(email_test_data["notif_down"].id)
    mock_resend.assert_called_once()
    args, kwargs = mock_resend.call_args
    assert args[0]["to"] == "email_test@example.com"
    assert args[0]["subject"] == "Down Alert"

@patch("app.services.email.resend.Emails.send")
def test_down_master_disabled(mock_resend, email_test_data, db_session):
    user = email_test_data["user"]
    user.email_notifications_enabled = False
    db_session.commit()
    
    send_notification_email_task(email_test_data["notif_down"].id)
    mock_resend.assert_not_called()

@patch("app.services.email.resend.Emails.send")
def test_down_alert_disabled(mock_resend, email_test_data, db_session):
    user = email_test_data["user"]
    user.down_alerts_enabled = False
    db_session.commit()
    
    send_notification_email_task(email_test_data["notif_down"].id)
    mock_resend.assert_not_called()

@patch("app.services.email.RESEND_API_KEY", "test_key")
@patch("app.services.email.resend.Emails.send")
def test_recovery_email_sent(mock_resend, email_test_data, db_session):
    mock_resend.return_value = {"id": "resend_id_123"}
    send_notification_email_task(email_test_data["notif_recovery"].id)
    mock_resend.assert_called_once()
    args, kwargs = mock_resend.call_args
    assert args[0]["to"] == "email_test@example.com"
    assert args[0]["subject"] == "Recovery Alert"

@patch("app.services.email.resend.Emails.send")
def test_recovery_master_disabled(mock_resend, email_test_data, db_session):
    user = email_test_data["user"]
    user.email_notifications_enabled = False
    db_session.commit()
    
    send_notification_email_task(email_test_data["notif_recovery"].id)
    mock_resend.assert_not_called()

@patch("app.services.email.resend.Emails.send")
def test_recovery_alert_disabled(mock_resend, email_test_data, db_session):
    user = email_test_data["user"]
    user.recovery_alerts_enabled = False
    db_session.commit()
    
    send_notification_email_task(email_test_data["notif_recovery"].id)
    mock_resend.assert_not_called()

@patch("app.services.email.RESEND_API_KEY", "test_key")
@patch("app.services.email.resend.Emails.send")
def test_resend_failure_logs_error(mock_resend, email_test_data, caplog):
    mock_resend.side_effect = Exception("Resend API Error")
    send_notification_email_task(email_test_data["notif_down"].id)
    assert "Error in send_notification_email_task: Resend API Error" in caplog.text
