import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.middleware import ERROR_MESSAGES, add_error_handling_middleware


@pytest.fixture
def app_with_middleware():
    app = FastAPI()
    add_error_handling_middleware(app)

    @app.get("/raise")
    def raise_generic():
        raise ValueError("Something went wrong")

    @app.get("/connection-error")
    def raise_connection():
        raise ConnectionError("Failed to connect")

    @app.get("/timeout-error")
    def raise_timeout():
        raise TimeoutError("Operation timed out")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


@pytest.fixture
def client(app_with_middleware):
    return TestClient(app_with_middleware, raise_server_exceptions=False)


def test_health_endpoint_works(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generic_error_returns_friendly_message(client):
    response = client.get("/raise")
    assert response.status_code == 500
    data = response.json()
    assert "error" in data
    assert "message" in data["error"]


def test_connection_error_returns_llm_unavailable(client):
    response = client.get("/connection-error")
    assert response.status_code == 500
    data = response.json()
    assert "学习引擎" in data["error"]["message"]


def test_timeout_error_returns_friendly_message(client):
    response = client.get("/timeout-error")
    assert response.status_code == 500
    data = response.json()
    assert "比预期长" in data["error"]["message"]


def test_error_messages_dict_has_all_codes():
    expected_codes = [
        "LLM_UNAVAILABLE",
        "INVALID_INPUT",
        "IMAGE_TOO_LARGE",
        "PAYLOAD_TOO_LARGE",
        "OCR_FAILED",
        "INTERNAL_ERROR",
    ]
    for code in expected_codes:
        assert code in ERROR_MESSAGES
        assert len(ERROR_MESSAGES[code]) > 0
