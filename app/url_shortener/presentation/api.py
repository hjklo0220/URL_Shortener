from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from url_shortener.infrastructure.dependencies import get_url_service
from url_shortener.application.services import URLService
from url_shortener.presentation.schemas import URLCreate, URLInfo, URLShorten
from config import settings

router = APIRouter()


@router.post("/shorten", response_model=URLShorten)
def create_short_url(
    url_create: URLCreate,
    service: URLService = Depends(get_url_service)
):
    url = service.create_short_url(url_create.url, url_create.expires_at)
    return URLShorten(short_url=f"{settings.BASE_URL}/{url.short_key}")

@router.get("/{short_key}")
def redirect_to_original_url(
    short_key: str,
    service: URLService = Depends(get_url_service)
):
    original_url = service.get_original_url(short_key)
    if original_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=original_url, status_code=301)

@router.get("/stats/{short_key}", response_model=URLInfo)
def get_url_stats(
    short_key: str,
    service: URLService = Depends(get_url_service)
):
    url = service.get_url_stats(short_key)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return URLInfo.from_domain(url)