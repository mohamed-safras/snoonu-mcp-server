import time
from functools import wraps
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter("snoonu_mcp_requests_total", "Total HTTP requests", ["method", "path", "status"])

REQUEST_LATENCY = Histogram("snoonu_mcp_request_duration_seconds", "HTTP request latency", ["method", "path"])

TOOL_CALL_COUNT = Counter("snoonu_mcp_tool_calls_total", "Total MCP tool calls", ["tool", "outcome"])

TOOL_CALL_LATENCY = Histogram("snoonu_mcp_tool_call_duration_seconds", "MCP tool call latency", ["tool"])

CACHE_HITS = Counter("snoonu_mcp_cache_hits_total", "Cache hits", ["fn"])

CACHE_MISSES = Counter("snoonu_mcp_cache_misses_total", "Cache misses", ["fn"])

DB_POOL_CHECKED_OUT = Gauge("snoonu_mcp_db_pool_checked_out", "DB connections currently checked out")

DB_POOL_SIZE = Gauge("snoonu_mcp_db_pool_size", "DB pool configured size")

ORDERS_CREATED = Counter("snoonu_mcp_orders_created_total", "Orders created")

ORDER_RATE_LIMITED = Counter("snoonu_mcp_orders_rate_limited_total", "Orders rejected by rate limiter")

def instrument_tool(name: str):
    """Records call count (by outcome) and latency for an MCP tool handler."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                TOOL_CALL_COUNT.labels(name, "success").inc()
                return result
            except Exception:
                TOOL_CALL_COUNT.labels(name, "error").inc()
                raise
            finally:
                TOOL_CALL_LATENCY.labels(name).observe(time.perf_counter() - start)
        return wrapper
    return decorator
