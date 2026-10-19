from fastapi.testclient import TestClient

from app.main import app


def test_provider_status_endpoint_returns_provider_statuses():
    client = TestClient(app)

    response = client.get("/api/providers/status")

    assert response.status_code == 200
    payload = response.json()
    providers = {provider["name"]: provider for provider in payload["providers"]}

    assert "gmail" in providers
    assert "microsoft" in providers
    assert providers["gmail"]["mode"] in {"demo", "configured"}
    assert providers["microsoft"]["mode"] in {"demo", "configured"}
    assert "status" in providers["gmail"]
    assert "status" in providers["microsoft"]
