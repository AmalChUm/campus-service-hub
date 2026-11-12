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
    assert response.get_json()["count"] == 5
