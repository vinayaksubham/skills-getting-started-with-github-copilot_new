import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response_unreg.status_code == 200
    assert response_unreg.json()["message"].startswith("Removed")
    # Unregister again should fail
    response_unreg2 = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert response_unreg2.status_code == 400


def test_signup_activity_full():
    activity = "Math Olympiad"
    # Fill up activity
    for i in range(8):
        email = f"student{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    # Should be full now
    response = client.post(f"/activities/{activity}/signup?email=extra@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]
