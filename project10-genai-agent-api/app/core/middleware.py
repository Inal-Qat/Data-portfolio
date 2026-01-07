import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.ids import new_request_id
from app.core.request_context import set_request_id

log = logging.getLogger("app.middleware")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = new_request_id()
        set_request_id(request_id)

        start = time.perf_counter()
        response = None

        try:
            response = await call_next(request)
            return response
        finally:
            duration_ms = int((time.perf_counter() - start) * 1000)

            log.info(
                "request_completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code if response else None,
                    "latency_ms": duration_ms,
                },
            )
