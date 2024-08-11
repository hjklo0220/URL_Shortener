import uuid

import base62

from url_shortener.application.interfaces import ShortenerService
from url_shortener.domain.value_objects import ShortKey


class Base62Shortener(ShortenerService):
    def __init__(self, length: int = 7):
        self.length = length

    def generate_short_key(self) -> ShortKey:
        # UUID를 생성하고 Base62로 인코딩
        uuid_int = uuid.uuid4().int
        encoded = base62.encodebytes(uuid_int.to_bytes(16, 'big'))

        return ShortKey(value=encoded[:self.length])

def get_shortener(length: int = 7) -> ShortenerService:
    return Base62Shortener(length)