import pytest
from app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_services_returns_seed_data(client):
    response = client.get("/services")
    assert response.status_code == 200
    assert any(item["id"] == "library" for item in response.get_json())


def test_service_lookup(client):
    response = client.get("/services/library")
    assert response.status_code == 200
    assert response.get_json()["name"] == "University Library"


def test_missing_service_is_not_found(client):
    response = client.get("/services/does-not-exist")
    assert response.status_code == 404
    assert response.get_json()["error"] == "service not found"


def test_category_filter(client):
    response = client.get("/services?category=academic")
    assert response.status_code == 200
    assert all(item["category"] == "academic" for item in response.get_json())


def test_name_search(client):
    response = client.get("/services?search=library")
    assert response.status_code == 200
    assert [item["id"] for item in response.get_json()] == ["library"]


def test_service_count(client):
    response = client.get("/services/count")
    assert response.status_code == 200
    assert response.get_json()["count"] == 6


import json
import os

def test_tutoring_service_data():
    """
    Verifies that the custom tutoring service exists in services.json
    and strictly conforms to the expected database schema.
    """
    # 1. Locate the services.json database file
    db_path = os.path.join(os.path.dirname(__file__), '../services.json')
    assert os.path.exists(db_path), "Database file services.json does not exist."

    # 2. Load database content
    with open(db_path, 'r') as file:
        database = json.load(file)

    # Extract the services list (assuming the JSON holds a {"services": [...]} dictionary)
    services_list = database.get("services", database) if isinstance(database, dict) else database

    # 3. Find the specific tutoring-01 service
    tutoring_entry = next((item for item in services_list if item.get("id") == "tutoring-01"), None)

    # Assert that the tutoring entry was successfully found
    assert tutoring_entry is not None, "Tutoring service with ID 'tutoring-01' was not found in services.json"

    # 4. Assert exact structural types and values for schema conformance
    assert isinstance(tutoring_entry["id"], str), "Field 'id' must be a string."
    assert tutoring_entry["id"] == "tutoring-01", "Field 'id' value must be 'tutoring-01'."

    assert isinstance(tutoring_entry["name"], str), "Field 'name' must be a string."
    assert any(keyword in tutoring_entry["name"].lower() for keyword in ["learning", "tutoring"]), "Field 'name' must contain 'learning' or 'tutoring'."
    #assert "tutoring" in tutoring_entry["name"].lower(), "Field 'name' must contain the word 'tutoring'."

    assert isinstance(tutoring_entry["category"], str), "Field 'category' must be a string."
    assert tutoring_entry["category"] == "learning-support", "Field 'category' must be set to 'learning-support'."
    #assert tutoring_entry["category"] == "academic", "Field 'category' must be set to 'academic'."

    assert isinstance(tutoring_entry["location"], str), "Field 'location' must be a string."
    assert len(tutoring_entry["location"]) > 0, "Field 'location' must not be empty."

    assert isinstance(tutoring_entry["hours"], str), "Field 'hours' must be a string."
    assert len(tutoring_entry["hours"]) > 0, "Field 'hours' must not be empty."

