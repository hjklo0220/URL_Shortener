from datetime import datetime

from fastapi.testclient import TestClient

from main import app
from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import OriginalURL, ShortKey
from url_shortener.infrastructure.dependencies import get_url_service
from config import settings

class MockURLService:
    def create_short_url(self, original_url: str, expires_at: datetime = None) -> URL:
        return URL(
            id=1,
            original_url=OriginalURL(value=original_url), 
            short_key=ShortKey(value="1234567"), 
            created_at=datetime.now(),
            expires_at=expires_at,
            views=0
        )

    def get_original_url(self, short_key: str) -> str:
        if short_key == "1234567":
            return "https://www.test.com"
        return None

    def get_url_stats(self, short_key: str) -> URL:
        if short_key == "1234567":
            return URL(
                id=1,
                original_url=OriginalURL(value="https://www.test.com"), 
                short_key=ShortKey(value="1234567"), 
                created_at=datetime.now(),
                expires_at=None,
                views=3
            )
        return None

    def delete_expired_urls(self) -> int:
        return 0

# 테스트를 위한 의존성 오버라이드
def override_get_url_service():
    return MockURLService()

app.dependency_overrides[get_url_service] = override_get_url_service

client = TestClient(app)

def test_create_short_url():
    response = client.post(f"{settings.API_PREFIX}/shorten", json={"url": "https://www.test.com"})
    assert response.status_code == 200
    assert "short_url" in response.json()
    assert response.json()["short_url"].endswith("/1234567")

def test_redirect_to_original_url():
    response = client.get(f"{settings.API_PREFIX}/1234567", allow_redirects=False)
    assert response.status_code == 301
    assert response.headers["Location"] == "https://www.test.com"

def test_redirect_to_nonexistent_url():
    response = client.get(f"{settings.API_PREFIX}/nonexistent", allow_redirects=False)
    assert response.status_code == 404

def test_get_url_stats():
    response = client.get(f"{settings.API_PREFIX}/stats/1234567")
    assert response.status_code == 200
    assert response.json()["short_key"] == "1234567"
    assert response.json()["views"] == 3

def test_get_nonexistent_url_stats():
    response = client.get(f"{settings.API_PREFIX}/stats/nonexistent")
    assert response.status_code == 404

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to URL Shortener API"}