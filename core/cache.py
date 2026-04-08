import redis
from core.config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def cache_set(key, value, expire=60):
    r.set(key, value, ex=expire)

def cache_get(key):
    return r.get(key)