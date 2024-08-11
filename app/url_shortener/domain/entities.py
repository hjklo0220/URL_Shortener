from datetime import datetime

from url_shortener.domain.value_objects import ShortKey, OriginalURL

class URL:
    def __init__(self, id: int, original_url: OriginalURL, short_key: ShortKey, 
                 created_at: datetime, expires_at: datetime | None, views: int):
        self.id = id
        self.original_url = original_url
        self.short_key = short_key
        self.created_at = created_at
        self.expires_at = expires_at
        self.views = views

    def is_expired(self) -> bool:
        return self.expires_at is not None and self.expires_at < datetime.now()

    def increment_views(self) -> None:
        self.views += 1

        