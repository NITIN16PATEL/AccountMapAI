import pytest
from fastapi.testclient import TestClient

from app.db.session import engine
from app.main import app
from app.models import Base

Base.metadata.create_all(bind=engine)
client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_returns_success():
    response = client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "securepass123"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "registered"


def test_register_rejects_short_password():
    response = client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "short"},
    )
    assert response.status_code == 400


def test_login_returns_demo_token():
    client.post(
        "/api/auth/register",
        json={"email": "user@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/api/auth/login",
        json={"email": "user@example.com", "password": "securepass123"},
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
