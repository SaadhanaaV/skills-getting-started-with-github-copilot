from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant_to_activity():
    response = client.post("/activities/Chess%20Club/signup?email=tester@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up tester@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "tester@mergington.edu" in activities_response.json()["Chess Club"]["participants"]


def test_signup_duplicate_participant_returns_400():
    email = "duplicate@mergington.edu"
    client.post(f"/activities/Programming%20Class/signup?email={email}")

    response = client.post(f"/activities/Programming%20Class/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant_from_activity():
    email = "remove-test@mergington.edu"
    client.post(f"/activities/Gym%20Class/signup?email={email}")

    response = client.delete(f"/activities/Gym%20Class/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Gym Class"

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert email not in activities_response.json()["Gym Class"]["participants"]


def test_remove_missing_participant_returns_404():
    response = client.delete(
        "/activities/Chess%20Club/participants?email=missing@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
