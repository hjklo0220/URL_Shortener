import aioredis

from app.url_shortener.application.interfaces.cache_service import CacheService
from config import settings

class RedisCache(CacheService):
    def __init__(self):
        self.redis = aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            encoding="utf-8",
            decode_responses=True
        )

    def get(self, key: str) -> str | None:
        return self.redis.get(key)

    def set(self, key: str, value: str, expire: int = 0):
        if expire > 0:
            self.redis.setex(key, expire, value)
        else:
            self.redis.set(key, value)

    def delete(self, key: str):
        self.redis.delete(key)

def get_cache() -> CacheService:
    return RedisCache()

