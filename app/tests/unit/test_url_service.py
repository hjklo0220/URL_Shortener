from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock

from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import OriginalURL, ShortKey
from url_shortener.application.services import URLService

class TestURLService(unittest.TestCase):
    def setUp(self):
        self.repository_mock = Mock()
        self.shortener_mock = Mock()
        self.service = URLService(self.repository_mock, self.shortener_mock)

    def test_create_short_url(self):
        original_url = "https://www.test.com"
        short_key = ShortKey(value="1234567")
        self.shortener_mock.generate_short_key.return_value = short_key

        created_url_entity = URL(
            id=1,
            original_url=OriginalURL(value=original_url),
            short_key=short_key,
            created_at=datetime.now(),
            expires_at=None,
            views=0
        )
        self.repository_mock.save.return_value = created_url_entity

        result: URL = self.service.create_short_url(original_url)

        self.shortener_mock.generate_short_key.assert_called_once()
        self.repository_mock.save.assert_called_once()
        self.assertEqual(result, created_url_entity)

    def test_get_original_url_existing(self):
        short_key = "1234567"
        original_url = "https://www.test.com"
        url = URL(
            id=1,
            original_url=OriginalURL(value=original_url),
            short_key=ShortKey(value=short_key),
            created_at=datetime.now(),
            expires_at=None,
            views=0
        )
        self.repository_mock.get_by_short_key.return_value = url

        result: str | None = self.service.get_original_url(short_key)

        self.repository_mock.get_by_short_key.assert_called_once_with(ShortKey(value=short_key))
        self.repository_mock.update.assert_called_once()
        self.assertEqual(result.rstrip('/'), original_url.rstrip('/'))
        self.assertEqual(url.views, 1)

    def test_get_original_url_no_existing(self):
        short_key = "noexist"
        self.repository_mock.get_by_short_key.return_value = None

        result: str | None = self.service.get_original_url(short_key)

        self.repository_mock.get_by_short_key.assert_called_once_with(ShortKey(value=short_key))
        self.assertIsNone(result)

    def test_get_original_url_expired(self):
        short_key = "expired"
        url = URL(
            id=1,
            original_url=OriginalURL(value="https://www.test.com"),
            short_key=ShortKey(value=short_key),
            created_at=datetime.now(),
            expires_at=datetime.now() - timedelta(days=1),
            views=0
        )
        self.repository_mock.get_by_short_key.return_value = url

        result: str | None = self.service.get_original_url(short_key)

        self.repository_mock.get_by_short_key.assert_called_once_with(ShortKey(value=short_key))
        self.assertIsNone(result)

    def test_get_url_stats(self):
        short_key = "1234567"
        url = URL(
            id=1,
            original_url=OriginalURL(value="https://www.test.com"),
            short_key=ShortKey(value=short_key),
            created_at=datetime.now(),
            expires_at=None,
            views=1
        )
        self.repository_mock.get_by_short_key.return_value = url

        result: URL = self.service.get_url_stats(short_key)

        self.repository_mock.get_by_short_key.assert_called_once_with(ShortKey(value=short_key))
        self.assertEqual(result, url)

    def test_delete_expired_urls(self):
        deleted_count = 1
        self.repository_mock.delete_expired.return_value = deleted_count

        result: int = self.service.delete_expired_urls()

        self.repository_mock.delete_expired.assert_called_once()
        self.assertEqual(result, deleted_count)




