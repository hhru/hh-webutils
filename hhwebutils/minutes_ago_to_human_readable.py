from datetime import datetime, timedelta


def convert_to_readable(minutes):
    now = datetime.now()
    stamp = now - timedelta(minutes=minutes)
    today_beginning = datetime(now.year, now.month, now.day)
    is_today = stamp > today_beginning

    diff = today_beginning - stamp
    diff_days = diff.days + 1

    if minutes == 0:
        time_code = 'online'
    elif is_today:
        time_code = 'today'
    elif diff_days == 1:
        time_code = 'yesterday'
    elif diff_days <= 7:
        time_code = 'weekExact'
    elif diff_days <= 30:
        time_code = 'week'
    else:
        time_code = 'month'

    return {
        'time_code': time_code,
        'days_ago': diff_days
    }
