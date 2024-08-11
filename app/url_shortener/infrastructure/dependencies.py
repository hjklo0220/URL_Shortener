from fastapi import Depends
from url_shortener.application.services import URLService
from url_shortener.infrastructure.database import get_db
from url_shortener.infrastructure.shortener import get_shortener
from url_shortener.infrastructure.repositories import SQLAlchemyURLRepository

def get_url_repository(db=Depends(get_db)):
    return SQLAlchemyURLRepository(db)

def get_url_service(
    repository=Depends(get_url_repository),
    shortener=Depends(get_shortener)
) -> URLService:
    return URLService(repository, shortener)