# coding=utf-8

from collections import namedtuple
from functools import reduce

DateInterval = namedtuple('DateInterval', ('start_date', 'end_date'))


def _get_date_interval_in_months(interval):
    start_date, end_date = interval
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1


def get_date_interval(start_date, end_date):
    return divmod(_get_date_interval_in_months((start_date, end_date)), 12)


def get_date_intervals_union(intervals):
    result_intervals = []

    def experience_union(interval1, interval2):
        if interval1.end_date >= interval2.start_date:
            if interval1.end_date > interval2.end_date:
                return interval1
            return DateInterval(interval1.start_date, interval2.end_date)
        result_intervals.append(interval1)
        return interval2

    result_intervals.append(reduce(experience_union, sorted(intervals)))
    return result_intervals


def get_date_intervals_sum(intervals):
    years, months = divmod(sum(_get_date_interval_in_months(i) for i in intervals), 12)
    split_years, months = divmod(months, 12)
    return years + split_years, months
