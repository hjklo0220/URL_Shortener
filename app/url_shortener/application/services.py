from datetime import datetime
from typing import Optional


from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import ShortKey, OriginalURL
from app.url_shortener.application.interfaces.url_repository import URLRepository
from app.url_shortener.application.interfaces.shortener_service import ShortenerService
from app.url_shortener.application.interfaces.cache_service import CacheService

class URLService:
    def __init__(self, repository: URLRepository, shortener: ShortenerService, cache: CacheService):
        self.repository = repository
        self.shortener = shortener
        self.cache = cache

    def create_short_url(self, original_url: str, expires_at: Optional[datetime] = None) -> URL:
        short_key = self.shortener.generate_short_key()
        url = URL(
            id=None,  #repository 에서
            original_url=OriginalURL(value=original_url),
            short_key=short_key,
            created_at=datetime.now(),
            expires_at=expires_at,
            views=0,
        )
        self.cache.set(short_key, original_url, expire=3600)
        saved_url = self.repository.save(url)
        return saved_url

    def get_original_url(self, short_key: str) -> Optional[str]:

        cached_url = self.cache.get(short_key)
        if cached_url:
            return cached_url
        
        url: URL = self.repository.get_by_short_key(ShortKey(value=short_key))
        if url and not url.is_expired():
            url.increment_views()
            self.repository.update(url)

            self.cache.set(short_key, str(url.original_url), expire=3600)
            
            return str(url.original_url)

        return None
    
    def get_url_stats(self, short_key: str) -> Optional[URL]:
        return self.repository.get_by_short_key(ShortKey(value=short_key))
    
    def delete_expired_urls(self) -> int:
        return self.repository.delete_expired(datetime.now())