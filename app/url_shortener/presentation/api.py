from fastapi import APIRouter, Depends

from url_shortener.infrastructure.dependencies import get_url_service
from url_shortener.application.services import URLService
from url_shortener.presentation.schemas import URLCreate, URLShorten
from config import settings

router = APIRouter()


@router.post("/shorten", response_model=URLShorten)
def create_short_url(
    url_create: URLCreate,
    service: URLService = Depends(get_url_service)
):
    url = service.create_short_url(url_create.url, url_create.expires_at)
    return URLShorten(short_url=f"{settings.BASE_URL}/{url.short_key}")
