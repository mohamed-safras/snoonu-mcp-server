import logging
import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.metrics import REQUEST_COUNT, REQUEST_LATENCY

logger = logging.getLogger("snoonu_mcp.requests")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        path = request.url.path
        REQUEST_COUNT.labels(request.method, path, response.status_code).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(duration_ms / 1000)

        logger.info(
            "%s %s — %.1fms [%s]",
            request.method, path, duration_ms, response.status_code,
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": path,
                "status": response.status_code,
                "duration_ms": round(duration_ms, 1),
            },
        )
        response.headers["x-request-id"] = request_id
        return response
