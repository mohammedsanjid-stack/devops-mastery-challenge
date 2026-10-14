
from unittest.mock import patch

from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "DevOps Mastery Challenge - Main Branch"
    assert response.json["status"] == "running"


@patch("app.get_db_connection")
def test_health(mock_get_connection):
    mock_connection = mock_get_connection.return_value
    mock_cursor = mock_connection.cursor.return_value.__enter__.return_value

    client = app.test_client()
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["database"] == "connected"
    mock_cursor.execute.assert_called_once_with("SELECT 1")
    mock_connection.close.assert_called_once()


@patch("app.get_db_connection", side_effect=Exception("Database unavailable"))
def test_health_database_unavailable(mock_get_connection):
    client = app.test_client()
    response = client.get("/api/health")

    assert response.status_code == 503
    assert response.json["status"] == "unhealthy"
    assert response.json["database"] == "disconnected"


def test_about():
    client = app.test_client()
    response = client.get("/api/about")

    assert response.status_code == 200
    assert response.json["project"] == "DevOps Mastery Challenge"
    assert response.json["version"] == "1.0.0"
    assert response.json["framework"] == "Flask"

