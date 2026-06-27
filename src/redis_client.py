import redis
from src.config.settings import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
