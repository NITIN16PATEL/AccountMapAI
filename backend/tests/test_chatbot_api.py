from fastapi.testclient import TestClient

from app.main import app


def test_chatbot_endpoint_returns_response_for_user_message():
    client = TestClient(app)

    response = client.post(
        "/api/chatbot/message",
        json={"message": "How do I check for suspicious accounts in my inventory?"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "reply" in payload
    assert len(payload["reply"]) > 0
    assert payload["mode"] in {"local", "configured"}
