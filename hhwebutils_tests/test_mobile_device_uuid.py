# coding=utf-8

import unittest

from hhwebutils.mobile_device_uuid import parse_uuid


class TestUrls(unittest.TestCase):
    user_agents_patterns = [
        'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID {}; ru.hh.iphone)',
        'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID: {}; ru.hh.iphone)',

        'Mozilla/5.0 (Linux; Android 8.0.0; AUM-L29 Build/HONORAUM-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 ru.hh.android/5.2.1.387, Device: AUM-L29, Android OS: '
        '8.0.0 (UUID: {})',

        'Mozilla/5.0 (Linux; Android 8.0.0; AUM-L29 Build/HONORAUM-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 ru.hh.android/5.2.1.387, Device: AUM-L29, Android OS: '
        '8.0.0 (UUID {})',

        'hh-justai-full-bot/1.0, channel: telegram UUID: {}',
        'hh-justai-full-bot/1.0, channel: telegram UUID {}',

        'bots (UUID: {})',
    ]

    def test_uppercase_uuid_parse(self):
        uuid_in_text = 'D7B64537-BFD1-4981-8B25-6C09E1163A3E'
        for ua in self.user_agents_patterns:
            self.assertEqual(uuid_in_text, parse_uuid(ua.format(uuid_in_text)))

    def test_lowercase_uuid_parse(self):
        uuid_in_text = 'd7b64537-bfd1-4981-8b25-6c09e1163a3e'
        for ua in self.user_agents_patterns:
            self.assertEqual(uuid_in_text.upper(), parse_uuid(ua.format(uuid_in_text)))

    def test_uuid_without_dashes_parse(self):
        uuid_in_text = '3922ad0a1b223fad50b8e43abb13cc35'
        for ua in self.user_agents_patterns:
            self.assertEqual(uuid_in_text.upper(), parse_uuid(ua.format(uuid_in_text)))

    def test_uuid_with_viber_user_id(self):
        uuid_in_text = 'bots__33680e3383079ef5e0c0d386719ce663b61003e3__vb__+Cs3kIt03ZrX/12Vu9PgA=='
        for ua in self.user_agents_patterns:
            self.assertEqual(uuid_in_text.upper(), parse_uuid(ua.format(uuid_in_text)))

    def test_no_uuid_value(self):
        self.assertIsNone(parse_uuid(
            'Mozilla/5.0 (Linux; Android 8.0.0; AUM-L29 Build/HONORAUM-L29; wv) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36'
        ))

    def test_none_argument(self):
        self.assertIsNone(parse_uuid(None))
