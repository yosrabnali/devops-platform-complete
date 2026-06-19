import pytest
from unittest.mock import patch, MagicMock
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    with patch("app.main.redis_client") as mock_redis:
        mock_redis.incr.return_value = 1
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
        assert "visits" in data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_metrics(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"flask_requests_total" in response.data

def test_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.get_json()
    assert "users" in data
    assert data["count"] == 3