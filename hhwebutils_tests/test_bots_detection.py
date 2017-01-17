import unittest

from hhwebutils import bots_detection


class TestBotDetector(unittest.TestCase):
    BOTS = {
        'YandexBot': 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'YandexAccessibilityBot': 'Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)'
    }

    def test_bots_detector(self):
        for bot_name, string in self.BOTS.iteritems():
            self.assertEqual(bots_detection.get_bot_name(string), bot_name)
