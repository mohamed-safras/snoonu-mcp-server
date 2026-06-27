import os
from src.redis_client import redis_client
from src.metrics import ORDER_RATE_LIMITED

MAX_PER_HOUR = int(os.environ.get("SNOONU_ORDER_MAX_PER_HOUR", "25"))
_KEY = "ratelimit:orders:hourly"

class OrderRateLimitError(Exception):
    pass

def check_rate_limit() -> None:
    count = redis_client.incr(_KEY)
    if count == 1:
        redis_client.expire(_KEY, 3600)
    if count > MAX_PER_HOUR:
        ORDER_RATE_LIMITED.inc()
        raise OrderRateLimitError("Too many orders this hour — try again later.")
