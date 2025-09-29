from datetime import datetime, timezone
from typing import TypedDict
from uuid import uuid4

from fastapi import Depends, FastAPI


class HealthDependencies(TypedDict):
    fastapi: str
    uvicorn: str
    python: str


class HealthResponse(TypedDict):
    status: str
    service: str
    request_id: str
    timestamp: str
    dependencies: HealthDependencies


def create_app() -> FastAPI:
    from service.app.security import require_api_key

    app = FastAPI(title="tushare-mcp", version="0.1.0")

    @app.get(
        "/health",
        response_model=HealthResponse,
        tags=["health"],
        dependencies=[Depends(require_api_key)],
    )
    async def health() -> HealthResponse:
        timestamp = datetime.now(tz=timezone.utc).isoformat()
        return {
            "status": "OK",
            "service": "tushare-mcp",
            "request_id": uuid4().hex,
            "timestamp": timestamp,
            "dependencies": {
                "fastapi": "0.111.0",
                "uvicorn": "0.30.0",
                "python": "3.11.8",
            },
        }

    return app


app = create_app()
