from datetime import datetime, timedelta
import unittest

from url_shortener.domain.entities import URL
from url_shortener.domain.value_objects import OriginalURL, ShortKey

class TestURL(unittest.TestCase):

    def setUp(self):
        self.original_url = OriginalURL(value="https://www.test.com")
        self.short_key = ShortKey(value="1234567")
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(days=7)
        self.url = URL(
            id=None,
            original_url=self.original_url,
            short_key=self.short_key,
            created_at=self.created_at,
            expires_at=self.expires_at,
            views=0
        )

    def test_initialization(self):
        self.assertEqual(self.url.id, None)
        self.assertEqual(self.url.original_url, self.original_url)
        self.assertEqual(self.url.short_key, self.short_key)
        self.assertEqual(self.url.created_at, self.created_at)
        self.assertEqual(self.url.expires_at, self.expires_at)
        self.assertEqual(self.url.views, 0)

    def test_is_expired_future(self):
        self.assertFalse(self.url.is_expired())

    def test_is_expired_past(self):
        self.url.expires_at = datetime.now() - timedelta(days=1)
        self.assertTrue(self.url.is_expired())

    def test_is_expired_none(self):
        self.url.expires_at = None
        self.assertFalse(self.url.is_expired())
    
    def test_increment_views(self):
        initial_views = self.url.views
        self.url.increment_views()
        self.assertEqual(self.url.views, initial_views + 1)

