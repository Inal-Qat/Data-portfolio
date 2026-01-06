from fastapi import Header, HTTPException
from app.core.config import settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    """
    If API_KEY is configured, require clients to pass it via X-API-Key header.
    If API_KEY is not configured, auth is disabled (useful for local dev).
    """
    if settings.API_KEY is None or settings.API_KEY == "":
        return

    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
