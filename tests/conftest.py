import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"][:],
        }
        for name, activity in activities.items()
    }

    activities.clear()
    activities.update(original_activities)

    yield

    activities.clear()
    activities.update(original_activities)
