from fastapi.testclient import TestClient

from app.main import app


def test_google_login_returns_demo_message_without_credentials():
    client = TestClient(app)

    response = client.get("/api/auth/google/login")

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "demo"
    assert "configured" in payload["message"].lower() or "demo" in payload["message"].lower()


def test_microsoft_login_returns_demo_message_without_credentials():
    client = TestClient(app)

    response = client.get("/api/auth/microsoft/login")

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "demo"
    assert "configured" in payload["message"].lower() or "demo" in payload["message"].lower()
