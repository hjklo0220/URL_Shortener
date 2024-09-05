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

    async def get(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def set(self, key: str, value: str, expire: int = 0):
        if expire > 0:
            await self.redis.setex(key, expire, value)
        else:
            await self.redis.set(key, value)

    async def delete(self, key: str):
        await self.redis.delete(key)

async def get_cache() -> CacheService:
    return RedisCache()

