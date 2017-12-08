# coding=utf-8

from unittest import TestCase

from hhwebutils_tests.device_detection_test_data import EXPECTED_DEVICE_TYPE_AND_UA, EXPECTED_IOS_VERSIONS_AND_UA
from hhwebutils.device_detection import get_device_type, ios_version


class TestMobileUtils(TestCase):

    def test_get_device_type(self):
        for expected_device, user_agent in EXPECTED_DEVICE_TYPE_AND_UA:
            self.assertEqual(expected_device,
                             get_device_type(user_agent),
                             'Unexpected device type for UA "{}"'.format(user_agent))

    def test_get_ios_version(self):
        for expected_version, user_agent in EXPECTED_IOS_VERSIONS_AND_UA:
            self.assertEqual(expected_version,
                             ios_version(user_agent),
                             'Unexpected device type for UA "{}"'.format(user_agent))
