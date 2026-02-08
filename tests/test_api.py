from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "UP"


def test_create_log():
    payload = {
        "level": "ERROR",
        "source": "test-service",
        "message": "database connection timeout"
    }

    response = client.post("/logs", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["level"] == "ERROR"
    assert "id" in data


def test_analyze_log():
    payload = {
        "level": "ERROR",
        "source": "test-service",
        "message": "database connection timeout"
    }

    log_resp = client.post("/logs", json=payload)
    log_id = log_resp.json()["id"]

    analyze_resp = client.post(f"/logs/{log_id}/analyze")
    assert analyze_resp.status_code == 200
    assert "category" in analyze_resp.json()
