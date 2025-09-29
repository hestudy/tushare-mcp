from datetime import datetime

from fastapi.testclient import TestClient

from service.app.main import app


client = TestClient(app)


def test_health_endpoint_returns_standard_payload() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()
    assert payload["status"] == "OK"
    assert payload["service"] == "tushare-mcp"

    request_id = payload["request_id"]
    assert isinstance(request_id, str)
    assert len(request_id) == 32

    timestamp = payload["timestamp"]
    parsed_timestamp = datetime.fromisoformat(timestamp)
    assert parsed_timestamp.tzinfo is not None

    dependencies = payload["dependencies"]
    assert dependencies == {
        "fastapi": "0.111.0",
        "uvicorn": "0.30.0",
        "python": "3.11.8",
    }
