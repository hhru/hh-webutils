# coding=utf-8
import re

IOS_RE = re.compile(r'iPad|iPhone|iPod', re.IGNORECASE)
ANDROID_RE = re.compile(r'Android', re.IGNORECASE)
WINDOWS_PHONE = re.compile(r'Windows Phone', re.IGNORECASE)
IOS_VERSION = re.compile(r'(?:iPhone|CPU)\sOS\s(\d+)_(\d+)', re.IGNORECASE)


class Device(object):
    IOS = u'ios'
    ANDROID = u'android'
    WINDOWS_PHONE = u'winphone'


def get_device_type(user_agent):
    # WP имеет в user agent строку "iPhone", поэтому детектим его сначала
    if re.search(WINDOWS_PHONE, user_agent):
        return Device.WINDOWS_PHONE

    if re.search(IOS_RE, user_agent):
        return Device.IOS

    if re.search(ANDROID_RE, user_agent):
        return Device.ANDROID

    return None


def ios_version(user_agent):
    if get_device_type(user_agent) != Device.IOS:
        return None

    version = re.search(IOS_VERSION, user_agent)
    if version is not None and len(version.groups()) > 1:
        return float(version.group(1) + '.' + version.group(2))
