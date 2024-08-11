from sqlalchemy.orm import Session

from url_shortener.domain.value_objects import OriginalURL, ShortKey
from url_shortener.domain.entities import URL
from url_shortener.application.interfaces import URLRepository
from url_shortener.infrastructure.database import URLModel


class SQLAlchemyURLRepository(URLRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, url: URL) -> URL:
        db_url = URLModel(
            original_url=str(url.original_url),
            short_key=str(url.short_key),
            created_at=url.created_at,
            expires_at=url.expires_at,
        )
        self.session.add(db_url)
        self.session.commit()
        self.session.refresh(db_url)
        return URL(
            id=db_url.id,
            original_url=db_url.original_url,
            short_key=db_url.short_key,
            created_at=db_url.created_at,
            expires_at=db_url.expires_at,
        )


def get_repository(session: Session) -> SQLAlchemyURLRepository:
    return SQLAlchemyURLRepository(session)
