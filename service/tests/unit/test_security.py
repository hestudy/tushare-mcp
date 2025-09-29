import pytest
from fastapi import HTTPException

from service.app.security import require_api_key, reset_rate_limiter
from shared.config.settings import reset_settings_cache


@pytest.fixture(autouse=True)
def _reset_security_state():
    reset_rate_limiter()
    reset_settings_cache()
    yield
    reset_rate_limiter()
    reset_settings_cache()


@pytest.mark.asyncio
async def test_require_api_key_rejects_missing_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "secret-value")
    reset_settings_cache()

    with pytest.raises(HTTPException) as exc_info:
        await require_api_key(api_key=None)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_require_api_key_allows_valid_key(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "secret-value")
    reset_settings_cache()

    await require_api_key(api_key="secret-value")


@pytest.mark.asyncio
async def test_rate_limiter_blocks_when_limit_exceeded(monkeypatch):
    monkeypatch.setenv("MCP_API_KEY", "secret-value")
    monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "1")
    reset_settings_cache()

    await require_api_key(api_key="secret-value")

    with pytest.raises(HTTPException) as exc_info:
        await require_api_key(api_key="secret-value")

    assert exc_info.value.status_code == 429
