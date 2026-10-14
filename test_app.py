from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "DevOps Mastery Challenge - Main Branch"
    assert response.json["status"] == "running"


def test_health():
    client = app.test_client()
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"
def test_about():
    client = app.test_client()
    response = client.get("/api/about")

    assert response.status_code == 200
    assert response.json["project"] == "DevOps Mastery Challenge"
    assert response.json["version"] == "1.0.0"
    assert response.json["framework"] == "Flask"
