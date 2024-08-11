from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl

from url_shortener.domain.entities import URL

class URLCreate(BaseModel):
    url: HttpUrl
    expires_at: Optional[datetime] = None

class URLShorten(BaseModel):
    short_url: str

