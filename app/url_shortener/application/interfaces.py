from abc import ABC, abstractmethod

from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import ShortKey, OriginalURL


class ShortenerService(ABC):
    @abstractmethod
    def generate_short_key(self) -> ShortKey:
        """short_key 생성"""
        pass

class URLRepository(ABC):
    @abstractmethod
    def save(self, url: URL) -> URL:
        """URL entity 저장"""
        pass

    @abstractmethod
    def get_by_short_key(self, short_key: ShortKey) -> URL:
        """short_key로 URL 검색"""
        pass
