# coding=utf-8

import unittest

from hhwebutils.uuid import parse_uuid


class TestUrls(unittest.TestCase):
    user_agents_patterns = [
        'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID {}; ru.hh.iphone)',
        'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID: {}; ru.hh.iphone)',

        'Mozilla/5.0 (Linux; Android 8.0.0; AUM-L29 Build/HONORAUM-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 ru.hh.android/5.2.1.387, Device: AUM-L29, Android OS: '
        '8.0.0 (UUID: {})',

        'Mozilla/5.0 (Linux; Android 8.0.0; AUM-L29 Build/HONORAUM-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36 ru.hh.android/5.2.1.387, Device: AUM-L29, Android OS: '
        '8.0.0 (UUID {})'
    ]

    def test_uppercase_uuid_parse(self):
        uuid_in_text = 'D7B64537-BFD1-4981-8B25-6C09E1163A3E'
        for ua in self.user_agents_patterns:
            self.assertEqual(uuid_in_text, parse_uuid(ua.format(uuid_in_text)))

    def test_lowercase_uuid_parse(self):
        uuid_in_text = 'd7b64537-bfd1-4981-8b25-6c09e1163a3e'
        for ua in self.user_agents_patterns:
            self.assertEqual(uuid_in_text, parse_uuid(ua.format(uuid_in_text)))

    def test_no_uuid_value(self):
        self.assertIsNone(parse_uuid(
            'Mozilla/5.0 (Linux; Android 8.0.0; AUM-L29 Build/HONORAUM-L29; wv) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36'
        ))
