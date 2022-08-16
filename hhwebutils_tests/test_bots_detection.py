import unittest

from hhwebutils import compat
from hhwebutils import bots_detection


class TestBotDetector(unittest.TestCase):
    BOTS = {
        'YandexBot': 'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
        'YandexAccessibilityBot': 'Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)'
    }

    def test_bots_detector(self):
        for bot_name, string in compat.iteritems(self.BOTS):
            self.assertEqual(bots_detection.get_bot_name(string), bot_name)

    def test_is_mobile_search_bot(self):
        bot_name = bots_detection.get_bot_name('Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')  # noqa
        self.assertTrue(bots_detection.is_mobile_search_bot(bot_name))
