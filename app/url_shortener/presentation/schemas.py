from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

from url_shortener.domain.entities import URL

class URLCreate(BaseModel):
    url: HttpUrl
    expires_at: Optional[datetime] = None

class URLShorten(BaseModel):
    short_url: str

class URLInfo(BaseModel):
    original_url: str
    short_key: str
    created_at: datetime
    expires_at: Optional[datetime]
    views: int

    @classmethod
    def from_domain(cls, url: URL):
        return cls(
            original_url=str(url.original_url),
            short_key=str(url.short_key),
            created_at=url.created_at,
            expires_at=url.expires_at,
            views=url.views
        )