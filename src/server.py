from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sqlalchemy import text
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from src.logging_config import configure_logging
from src.middleware import RequestLoggingMiddleware
from src.tools import products, categories, delivery, orders
from src.api.database.session import engine
from src.metrics import DB_POOL_CHECKED_OUT, DB_POOL_SIZE
from src.config.settings import settings

configure_logging()


# stateless_http=True: each request is independent of which worker handles it.
# Without this, MCP session IDs are pinned to the worker process that created them,
# so running >1 Gunicorn worker silently breaks clients ("Session terminated") the
# moment a follow-up request lands on a different worker.
mcp = FastMCP(
    "snoonu-mcp-server",
    stateless_http=True,
    transport_security=TransportSecuritySettings(allowed_hosts=settings.allowed_hosts),
)

products.register(mcp)
categories.register(mcp)
delivery.register(mcp)
orders.register(mcp)

async def health(_request: Request) -> Response:
    return JSONResponse({"status": "ok"})

async def ready(_request: Request) -> Response:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        return JSONResponse({"status": "unavailable", "error": str(exc)}, status_code=503)
    return JSONResponse({"status": "ready"})

async def metrics(_request: Request) -> Response:
    DB_POOL_CHECKED_OUT.set(engine.pool.checkedout())
    DB_POOL_SIZE.set(settings.db_pool_size)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app = mcp.streamable_http_app()
app.routes.extend([
    Route("/health", health),
    Route("/ready", ready),
    Route("/metrics", metrics),
])
app.add_middleware(RequestLoggingMiddleware)
