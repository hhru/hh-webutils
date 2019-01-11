# coding=utf-8

import unittest

from hhwebutils.uuid import parse_uuid


class TestUrls(unittest.TestCase):

    def test_uppercase_uuid_parse(self):
        uuid_in_text = 'D7B64537-BFD1-4981-8B25-6C09E1163A3E'
        parsed_uuid = parse_uuid(
            'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID {}; ru.hh.iphone)'.format(uuid_in_text)
        )
        self.assertEqual(uuid_in_text, parsed_uuid)

    def test_lowercase_uuid_parse(self):
        uuid_in_text = 'd7b64537-bfd1-4981-8b25-6c09e1163a3e'
        parsed_uuid = parse_uuid(
            'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID {}; ru.hh.iphone)'.format(uuid_in_text)
        )
        self.assertEqual(uuid_in_text, parsed_uuid)

    def test_no_uuid_in_text(self):
        uuid_in_text = 'СОВСЕМ-НЕ-ПОХОЖЕ-НА-UUID'
        parsed_uuid = parse_uuid(
            'ApplicantHH (iPhone 6 Plus; iOS 11.1.2; Version/5.1.1812.885; UUID {}; ru.hh.iphone)'.format(uuid_in_text)
        )
        self.assertIsNone(parsed_uuid)
