# coding=utf-8
from hhwebutils.huawei_devices import HUAWEI_DEVICES


def normalize(text):
    return text.replace(' ', '').upper()


_HUAWEI_DEVICES = [normalize(device) for device in HUAWEI_DEVICES]


def is_huawei_device(user_agent):
    if user_agent is None:
        return False
    user_agent = normalize(user_agent)
    for device in _HUAWEI_DEVICES:
        if device in user_agent:
            return True
    return False
