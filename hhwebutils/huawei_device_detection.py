# coding=utf-8
import re

_HUAWEI_DEVICES = [
    'LIO-L29',
    'TAH-N29m',
    'ELS-N39',
    'ELS-NX9',
    'ANA-NX9',
    'CDY-NX9A',
    'JEF-NX9',
    'JNY-LX1',
    'ART-L29N',
    'AQM-LX1',
    'MED-LX9N',
    'DRA-LX9',
    'MRX-W09',
    'Bach3-W09',
    'Schumann-W0',
    'AgassiR-W09B',
    'Agassi3-L09A',
    'KOB2-W09',
    'OXF-AN10',
    'BMH-AN10',
    'EBG-AN10',
    'CDY-NX9A',
    'MOA-LX9N',
    'AKA-L29',
    'DUA-LX9',
    'FRH-L21',
    'DDG-LX9',
    'LRA-LX1',
    'AGR-AL09HN',
    'AGS3-AL09HN',
    'KRJ-W09',
]

_HUAWEI_DEVICES = [re.compile(pattern) for pattern in _HUAWEI_DEVICES]


def is_huawei_device(user_agent):
    if user_agent is None:
        return False
    for regexp in _HUAWEI_DEVICES:
        if regexp.search(user_agent) is not None:
            return True
    return False
