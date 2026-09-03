import pytest
from datetime import datetime
from app.models import User, Notification
from app.core.security import create_access_token, hash_password

def test_update_profile_name(client, db_session):
    user = User(
        name="Original Name",
        email="profiletest@example.com",
        password=hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Update name to valid string
    res = client.patch(
        "/api/auth/profile",
        headers=headers,
        json={"name": "  Updated Dev Name  "},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Updated Dev Name"
    assert data["email"] == "profiletest@example.com"
    assert data["id"] == user.id

    # Verify database was updated
    db_session.refresh(user)
    assert user.name == "Updated Dev Name"


def test_update_profile_validation(client, db_session):
    user = User(
        name="Valid Name",
        email="validname@example.com",
        password=hash_password("password123"),
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Empty / whitespace-only name should return 422
    res_empty = client.patch(
        "/api/auth/profile",
        headers=headers,
        json={"name": "   "},
    )
    assert res_empty.status_code == 422
    assert "Name cannot be empty" in res_empty.json()["detail"]

    # Name > 100 characters should return 422
    long_name = "A" * 105
    res_long = client.patch(
        "/api/auth/profile",
        headers=headers,
        json={"name": long_name},
    )
    assert res_long.status_code == 422
    assert "Name must not exceed 100 characters" in res_long.json()["detail"]


def test_get_and_patch_preferences_endpoints(client, db_session):
    user = User(
        name="Pref User",
        email="prefuser@example.com",
        password=hash_password("password123"),
        email_notifications_enabled=True,
        down_alerts_enabled=True,
        recovery_alerts_enabled=True,
    )
    db_session.add(user)
    db_session.commit()

    token = create_access_token(user.id)
    headers = {"Authorization": f"Bearer {token}"}

    # Test GET /api/auth/preferences
    res_get_auth = client.get("/api/auth/preferences", headers=headers)
    assert res_get_auth.status_code == 200
    assert res_get_auth.json()["email_notifications_enabled"] is True

    # Test GET /api/notifications/preferences
    res_get_notif = client.get("/api/notifications/preferences", headers=headers)
    assert res_get_notif.status_code == 200
    assert res_get_notif.json()["email_notifications_enabled"] is True

    # Test PATCH /api/notifications/preferences
    res_patch_notif = client.patch(
        "/api/notifications/preferences",
        headers=headers,
        json={"down_alerts_enabled": False},
    )
    assert res_patch_notif.status_code == 200
    assert res_patch_notif.json()["down_alerts_enabled"] is False

    # Verify GET /api/auth/preferences reflects update
    res_get_updated = client.get("/api/auth/preferences", headers=headers)
    assert res_get_updated.json()["down_alerts_enabled"] is False

