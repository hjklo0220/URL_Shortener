from abc import ABC, abstractmethod
from typing import Optional

class CacheService(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        """캐시에서 값 가져옴"""
        pass

    @abstractmethod
    async def set(self, key: str, value: str, expire: int = 0):
        """캐시에 값 저장"""
        pass

    @abstractmethod
    async def delete(self, key: str):
        """캐시에서 값 삭제"""
        pass