from abc import ABC, abstractmethod

from app.url_shortener.domain.value_objects import ShortKey

class ShortenerService(ABC):
    @abstractmethod
    def generate_short_key(self) -> ShortKey:
        """short_key 생성"""
        pass