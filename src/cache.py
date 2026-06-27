import json
from functools import wraps
from src.redis_client import redis_client
from src.metrics import CACHE_HITS, CACHE_MISSES

def cached(ttl_seconds: int):
    """Redis-backed TTL cache for read-mostly tool handlers, shared across workers/replicas."""
    def decorator(fn):
        prefix = f"cache:{fn.__module__}.{fn.__qualname__}"

        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = f"{prefix}:{args}:{sorted(kwargs.items())}"
            cached_value = redis_client.get(key)
            if cached_value is not None:
                CACHE_HITS.labels(fn.__qualname__).inc()
                return json.loads(cached_value)
            CACHE_MISSES.labels(fn.__qualname__).inc()
            result = fn(*args, **kwargs)
            redis_client.set(key, json.dumps(result), ex=ttl_seconds)
            return result
        return wrapper
    return decorator