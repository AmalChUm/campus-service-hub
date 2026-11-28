import json

import pytest

import app as app_module
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


def names(response):
    return [item["name"] for item in response.get_json()]


def test_sort_by_name_ascending(client):
    response = client.get("/services?sort=name")
    assert response.status_code == 200
    assert len(response.get_json()) == 5
    assert names(response) == sorted(names(client.get("/services")), key=str.lower)
    assert names(response)[0] == "Academic Advising"


def test_sort_by_name_descending(client):
    response = client.get("/services?sort=-name")
    assert response.status_code == 200
    assert len(response.get_json()) == 5
    assert names(response) == sorted(names(client.get("/services")), key=str.lower, reverse=True)
    assert names(response)[0] == "University Library"


def test_sort_works_with_category_filter(client):
    ascending = client.get("/services?category=academic&sort=name")
    descending = client.get("/services?category=academic&sort=-name")
    assert names(ascending) == ["Academic Advising", "Peer Tutoring Center", "University Library"]
    assert names(descending) == ["University Library", "Peer Tutoring Center", "Academic Advising"]


def test_sort_works_with_search_filter(client):
    response = client.get("/services?search=center&sort=-name")
    assert response.status_code == 200
    assert names(response) == ["Peer Tutoring Center"]


@pytest.mark.parametrize("value", ["bogus", "category", "NAME", ""])
def test_invalid_sort_returns_400(client, value):
    response = client.get(f"/services?sort={value}")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_invalid_sort_with_filter_still_returns_400(client):
    response = client.get("/services?category=academic&sort=bogus")
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_sort_is_case_insensitive(client, tmp_path, monkeypatch):
    data = [
        {"id": "b", "name": "beta lab", "category": "academic", "location": "x", "hours": "1-2"},
        {"id": "a", "name": "Alpha Lab", "category": "academic", "location": "x", "hours": "1-2"},
        {"id": "c", "name": "charlie lab", "category": "academic", "location": "x", "hours": "1-2"},
    ]
    path = tmp_path / "services.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(app_module, "DATA_FILE", path)
    assert names(client.get("/services?sort=name")) == ["Alpha Lab", "beta lab", "charlie lab"]
    assert names(client.get("/services?sort=-name")) == ["charlie lab", "beta lab", "Alpha Lab"]


def test_no_sort_keeps_original_order(client):
    ids = [item["id"] for item in client.get("/services").get_json()]
    assert ids == ["library", "advising", "tutoring", "health", "it-support"]