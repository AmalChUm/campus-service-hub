import pytest
from app import MAX_FILTER_LENGTH, app


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


def ids(response):
    return [item["id"] for item in response.get_json()]


@pytest.mark.parametrize("value", ["", "   ", "%20%20%20", "%09"])
def test_blank_category_is_ignored(client, value):
    response = client.get(f"/services?category={value}")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


@pytest.mark.parametrize("value", ["", "   ", "%20%20%20", "%09"])
def test_blank_search_is_ignored(client, value):
    response = client.get(f"/services?search={value}")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_blank_category_and_search_together_are_ignored(client):
    response = client.get("/services?category=%20&search=%20%20")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_filter_values_are_trimmed(client):
    assert ids(client.get("/services?category=%20academic%20")) == ["library", "advising", "tutoring"]
    assert ids(client.get("/services?search=%20library%20")) == ["library"]


def test_filtering_is_still_case_insensitive(client):
    assert ids(client.get("/services?category=ACADEMIC")) == ["library", "advising", "tutoring"]
    assert ids(client.get("/services?search=LiBrArY")) == ["library"]


@pytest.mark.parametrize("name", ["category", "search"])
def test_value_at_maximum_length_is_accepted(client, name):
    response = client.get(f"/services?{name}=" + "a" * MAX_FILTER_LENGTH)
    assert response.status_code == 200
    assert response.get_json() == []


@pytest.mark.parametrize("name", ["category", "search"])
def test_value_over_maximum_length_is_rejected(client, name):
    response = client.get(f"/services?{name}=" + "a" * (MAX_FILTER_LENGTH + 1))
    assert response.status_code == 400
    assert "error" in response.get_json()


@pytest.mark.parametrize("name", ["category", "search"])
def test_padding_does_not_count_toward_maximum_length(client, name):
    padded = "%20%20" + "a" * MAX_FILTER_LENGTH + "%20%20"
    response = client.get(f"/services?{name}={padded}")
    assert response.status_code == 200


def test_over_limit_value_is_rejected_even_with_a_valid_other_filter(client):
    response = client.get("/services?category=academic&search=" + "b" * (MAX_FILTER_LENGTH + 1))
    assert response.status_code == 400
    assert "error" in response.get_json()