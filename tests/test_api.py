from unittest.mock import patch

from fastapi.testclient import TestClient

from wmax.main import app

client = TestClient(app)


def test_calculate_endpoint() -> None:
    response = client.post("/api/calculate", json={"weight": 100, "reps": 6, "mode": 1})
    assert response.status_code == 200
    data = response.json()
    assert "maximum" in data
    assert data["weight"] == 100
    assert data["reps"] == 6
    assert data["mode"] == 1


def test_calculate_invalid_data() -> None:
    response = client.post("/api/calculate", json={"weight": 0, "reps": 6, "mode": 1})
    assert response.status_code == 422


def test_calculate_value_error() -> None:
    # Test the ValueError block directly by mocking calculate_1rm
    with patch("wmax.api.calculate_1rm", side_effect=ValueError("Mocked error")):
        response = client.post("/api/calculate", json={"weight": 100, "reps": 6, "mode": 1})
        assert response.status_code == 400
        assert response.json()["detail"] == "Mocked error"


def test_index_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
