"""安全与速率限制工具。

该模块提供 API Key 校验与简单的基于窗口的速率限制器。
"""

from __future__ import annotations

import secrets
import time
from collections import deque
from threading import Lock

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

from shared.config.settings import get_settings

_API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


class RateLimiter:
    """简单的固定时间窗口速率限制器。"""

    def __init__(self) -> None:
        self._lock = Lock()
        self._requests: deque[float] = deque()

    def allow(self, limit: int, window_seconds: int = 60) -> bool:
        """当窗口内请求数未超过限制时返回 True。"""

        now = time.monotonic()
        cutoff = now - window_seconds

        with self._lock:
            while self._requests and self._requests[0] <= cutoff:
                self._requests.popleft()

            if len(self._requests) >= limit:
                return False

            self._requests.append(now)
            return True

    def reset(self) -> None:
        with self._lock:
            self._requests.clear()


_rate_limiter = RateLimiter()


async def require_api_key(api_key: str | None = Security(_API_KEY_HEADER)) -> None:
    """校验请求头中的 API Key，并应用速率限制。"""

    settings = get_settings()
    expected_api_key = settings.api_key
    rate_limit = settings.rate_limit_per_minute

    if expected_api_key:
        if not api_key or not secrets.compare_digest(api_key, expected_api_key):
            raise HTTPException(status_code=401, detail="Invalid or missing API key")

    if rate_limit and rate_limit > 0:
        if not _rate_limiter.allow(rate_limit):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")


def reset_rate_limiter() -> None:
    """清空速率限制器状态，便于测试复现。"""

    _rate_limiter.reset()
