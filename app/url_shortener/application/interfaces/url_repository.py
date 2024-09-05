import datetime
from abc import ABC, abstractmethod

from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import ShortKey


class URLRepository(ABC):
    @abstractmethod
    def save(self, url: URL) -> URL:
        """URL entity 저장"""
        pass

    @abstractmethod
    def get_by_short_key(self, short_key: ShortKey) -> URL:
        """short_key로 URL 검색"""
        pass

    @abstractmethod
    def update(self, url: URL) -> URL:
        """조회수 업데이트"""
        pass

    @abstractmethod
    def delete_expired(self, current_time: datetime) -> int:
        """만료된 URL들 삭제"""
        pass
