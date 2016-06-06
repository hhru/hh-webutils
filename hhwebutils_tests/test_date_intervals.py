# coding=utf-8

from datetime import datetime
import unittest

from hhwebutils import date_intervals


class TestDateIntervals(unittest.TestCase):

    def test_get_date_interval(self):
        self.assertEqual(date_intervals.get_date_interval(datetime(2010, 10, 30), datetime(2012, 10, 30)), (2, 1))
        self.assertEqual(date_intervals.get_date_interval(datetime(2012, 10, 30), datetime(2012, 11, 30)), (0, 2))
        self.assertEqual(date_intervals.get_date_interval(datetime(2012, 10, 30), datetime(2012, 10, 30)), (0, 1))
        self.assertEqual(date_intervals.get_date_interval(datetime(2012, 10, 29), datetime(2012, 10, 30)), (0, 1))

    def test_get_date_intervals_union(self):
        intervals = [
            date_intervals.DateInterval(datetime(2012, 1, 1), datetime(2012, 2, 1)),
            date_intervals.DateInterval(datetime(2012, 2, 1), datetime(2012, 3, 1)),
            date_intervals.DateInterval(datetime(2012, 3, 15), datetime(2012, 5, 15)),
            date_intervals.DateInterval(datetime(2012, 4, 15), datetime(2012, 7, 15)),
            date_intervals.DateInterval(datetime(2012, 8, 1), datetime(2012, 12, 1)),
            date_intervals.DateInterval(datetime(2012, 9, 1), datetime(2012, 10, 1)),
        ]

        result = [
            date_intervals.DateInterval(datetime(2012, 1, 1), datetime(2012, 3, 1)),
            date_intervals.DateInterval(datetime(2012, 3, 15), datetime(2012, 7, 15)),
            date_intervals.DateInterval(datetime(2012, 8, 1), datetime(2012, 12, 1)),
        ]

        self.assertEqual(date_intervals.get_date_intervals_union(intervals), result)

        intervals = [date_intervals.DateInterval(datetime(2012, 1, 1), datetime(2012, 2, 1))]
        result = [date_intervals.DateInterval(datetime(2012, 1, 1), datetime(2012, 2, 1))]

        self.assertEqual(date_intervals.get_date_intervals_union(intervals), result)

    def test_get_date_intervals_sum(self):
        intervals = [
            date_intervals.DateInterval(datetime(2012, 1, 1), datetime(2012, 3, 1)),
            date_intervals.DateInterval(datetime(2012, 3, 15), datetime(2012, 7, 15)),
            date_intervals.DateInterval(datetime(2012, 8, 1), datetime(2012, 12, 1)),
        ]

        self.assertEqual(date_intervals.get_date_intervals_sum(intervals), (1, 1))

        self.assertEqual(date_intervals.get_date_intervals_sum(
            [date_intervals.DateInterval(datetime(2012, 1, 1), datetime(2012, 3, 1))]),
            (0, 3)
        )
        self.assertEqual(date_intervals.get_date_intervals_sum([]), (0, 0))
