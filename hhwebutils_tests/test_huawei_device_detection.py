# coding=utf-8
import unittest

from hhwebutils import compat
from hhwebutils import huawei_device_detection


class TestHuaweiDeviceDetection(unittest.TestCase):
    DEVICES = {
        'Mozilla/5.0 (Linux; Android 9; LIO-L29) AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/73.0.3683.90 Mobile Safari/537.36': True,
        'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0_1 like Mac OS X) ' +
        'AppleWebKit/536.26 (KHTML, like Gecko) Mobile/10A523': False,
        'HUAWEI LUA-L01': True,
        'HuAwEI HoNoR V9': True,
        'HUAWEI-HONOR-V9': False,
        None: False,
    }

    def test_huawei_device(self):
        for user_agent, is_huawei in compat.iteritems(self.DEVICES):
            self.assertEqual(huawei_device_detection.is_huawei_device(user_agent), is_huawei)
