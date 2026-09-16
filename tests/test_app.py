from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    original_participants = list(activities[activity_name]["participants"])

    response = client.post(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities[activity_name]["participants"] = original_participants


def test_unregister_participant_fails_for_unregistered_email():
    response = client.post("/activities/Chess Club/unregister?email=student@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
