import unittest

from url_shortener.infrastructure.shortener import Base62Shortener
from url_shortener.domain.value_objects import ShortKey

class TestBase62Shortener(unittest.TestCase):
    def setUp(self):
        self.shortener = Base62Shortener()

    def test_generate_short_key_length(self):
        short_key = self.shortener.generate_short_key()
        self.assertEqual(len(short_key.value), 7)

    def test_generate_short_key_unique(self):
        short_keys = set()
        # 1000개의 키를 생성하여 중복 검사
        for _ in range(1000):
            short_key = self.shortener.generate_short_key()
            self.assertNotIn(short_key.value, short_keys)
            short_keys.add(short_key.value)

    def test_generate_short_key(self):
        short_key = self.shortener.generate_short_key()
        
        self.assertIsInstance(short_key, ShortKey)

