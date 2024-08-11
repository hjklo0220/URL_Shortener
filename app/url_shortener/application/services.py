from datetime import datetime
from typing import Optional

from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import OriginalURL
from url_shortener.application.interfaces import URLRepository, ShortenerService

class URLService:
    def __init__(self, repository: URLRepository, shortener: ShortenerService):
        self.repository = repository
        self.shortener = shortener

    def create_short_url(self, original_url: str, expires_at: Optional[datetime] = None) -> URL:
        short_key = self.shortener.generate_short_key()
        url = URL(
            id=None,  #repository 에서
            original_url=OriginalURL(value=original_url),
            short_key=short_key,
            created_at=datetime.now(),
            expires_at=expires_at,
        )
        saved_url = self.repository.save(url)
        return saved_url

    def get_original_url(self, short_key: str) -> Optional[str]:
        ...

        return None