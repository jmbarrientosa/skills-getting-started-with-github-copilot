from src.app import activities


class TestRootEndpoint:
    def test_root_redirects_to_static(self, client):
        response = client.get("/", follow_redirects=False)

        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    def test_get_activities_returns_all_activities(self, client):
        response = client.get("/activities")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_activities_include_required_fields(self, client):
        response = client.get("/activities")

        data = response.json()
        for activity_data in data.values():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)


class TestSignupEndpoint:
    def test_signup_adds_participant(self, client):
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"},
        )

        assert response.status_code == 200
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

    def test_signup_rejects_duplicate(self, client):
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_rejects_unknown_activity(self, client):
        response = client.post(
            "/activities/Unknown Club/signup",
            params={"email": "student@mergington.edu"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"


class TestUnregisterEndpoint:
    def test_unregister_removes_participant(self, client):
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "michael@mergington.edu"},
        )

        assert response.status_code == 200
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    def test_unregister_rejects_unknown_participant(self, client):
        response = client.delete(
            "/activities/Chess Club/participants",
            params={"email": "missing@mergington.edu"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
