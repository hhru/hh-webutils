# coding=utf-8

import unittest
from datetime import datetime, date, time
from freezegun import freeze_time

from hhwebutils.minutes_ago_to_human_readable import convert_to_readable


def get_day_minutes_since_start():
    now = datetime.now()
    today_beginning = datetime(now.year, now.month, now.day)
    diff = now - today_beginning
    return int(diff.seconds / 60)


@freeze_time("2018-07-03 00:10:01")
class TestMinutesAgoConversion(unittest.TestCase):
    def check(self, diff, time_code, days_ago):
        self.assertEqual(convert_to_readable(diff), {'time_code': time_code, 'days_ago': days_ago})

    def test_format(self):
        self.assertEqual(convert_to_readable(0), {'time_code': 'online', 'days_ago': 0})

    def test_time_codes(self):
        start_minutes = get_day_minutes_since_start()
        full_day_minutes = 60 * 24

        self.check(0, 'online', 0)
        self.check(5, 'today', 0)
        self.check(10, 'today', 0)
        self.check(start_minutes, 'today', 0)
        self.check(start_minutes + 1, 'yesterday', 1)
        self.check(start_minutes + full_day_minutes, 'yesterday', 1)
        self.check(start_minutes + full_day_minutes + 1, 'weekExact', 2)
        self.check(start_minutes + (full_day_minutes * 7), 'weekExact', 7)
        self.check(start_minutes + (full_day_minutes * 7) + 1, 'week', 8)
        self.check(start_minutes + (full_day_minutes * 30), 'week', 30)
        self.check(start_minutes + (full_day_minutes * 30) + 1, 'month', 31)
        self.check(start_minutes + (full_day_minutes * 100), 'month', 100)
