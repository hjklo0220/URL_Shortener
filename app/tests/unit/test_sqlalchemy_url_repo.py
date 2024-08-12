import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from sqlalchemy.orm import Session

from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import OriginalURL, ShortKey
from url_shortener.infrastructure.database import URLModel
from url_shortener.infrastructure.repositories import SQLAlchemyURLRepository

class TestSQLAlchemyURLRepository(unittest.TestCase):
    def setUp(self):
        self.session = Mock(spec=Session)
        self.repository = SQLAlchemyURLRepository(self.session)

    def test_save(self):
        url = URL(
            id=None, 
            original_url=OriginalURL(value="https://www.test.com"), 
            short_key=ShortKey(value="1234567"),
            created_at=datetime.now(), 
            expires_at=None, 
            views=0
            )
        
        db_url = Mock(spec=URLModel)
        db_url.id = 1
        db_url.original_url = str(url.original_url)
        db_url.short_key = str(url.short_key)
        db_url.created_at = url.created_at
        db_url.expires_at = url.expires_at
        db_url.views = url.views

        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None
        
        # patch.object를 사용하여 도메인 객체 변환 로직 대체
        with patch.object(self.repository, '_to_domain', return_value=url):
            result: URL = self.repository.save(url)

        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertEqual(result, url)

    def test_update(self):
        url = URL(
            id=None, 
            original_url=OriginalURL(value="https://www.test.com"), 
            short_key=ShortKey(value="1234567"),
            created_at=datetime.now(), 
            expires_at=None, 
            views=0
            )
        
        db_url = Mock(spec=URLModel)
        db_url.id = url.id
        db_url.views = url.views

        # 쿼리 체인 모킹
        self.session.query.return_value.filter.return_value.first.return_value = db_url

        self.session.commit.return_value = None
        self.session.refresh.return_value = None
        
        with patch.object(self.repository, '_to_domain', return_value=url):
            result: URL = self.repository.update(url)

        self.session.query.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once()
        self.assertEqual(result, url)

    def test_get_by_short_key(self):
        short_key = ShortKey(value="1234567")
        db_url = Mock(spec=URLModel)
        
        self.session.query.return_value.filter.return_value.first.return_value = db_url
        
        url = URL(
            id=None, 
            original_url=OriginalURL(value="https://www.test.com"), 
            short_key=ShortKey(value="1234567"),
            created_at=datetime.now(), 
            expires_at=None, 
            views=0
            )
        
        with patch.object(self.repository, '_to_domain', return_value=url):
            result: URL = self.repository.get_by_short_key(short_key)

        self.session.query.assert_called_once()
        self.assertEqual(result, url)

    def test_delete_expired(self):
        current_time = datetime.now()
        mock_result = Mock()
        mock_result.rowcount = 5
        
        self.session.execute.return_value = mock_result
        self.session.commit.return_value = None

        result: int = self.repository.delete_expired(current_time)

        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertEqual(result, 5)
