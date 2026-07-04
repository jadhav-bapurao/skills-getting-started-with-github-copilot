from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_activity_list():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_participant_for_activity():
    response = client.post(
        "/activities/Chess Club/signup?email=teststudent@mergington.edu"
    )
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "teststudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_duplicate_signup_is_rejected():
    response = client.post(
        "/activities/Chess Club/signup?email=teststudent@mergington.edu"
    )
    assert response.status_code == 400
    assert response.json()[
        "detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_404():
    response = client.post(
        "/activities/Unknown Activity/signup?email=student@example.com")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_from_activity():
    response = client.delete(
        "/activities/Chess Club/unregister?email=teststudent@mergington.edu"
    )
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "teststudent@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.delete(
        "/activities/Chess Club/unregister?email=missing@example.com"
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
