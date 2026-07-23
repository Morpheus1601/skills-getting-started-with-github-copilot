import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def restore_state():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(original)


@pytest.fixture()
def client():
    return TestClient(app_module.app)


def test_unregister_participant_removes_student_from_activity(client):
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" in response.json()["message"]

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
