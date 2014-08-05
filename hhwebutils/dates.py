import datetime
import dateutil.parser
import time


def add_client_utc_offset_to_server_iso_date(iso_date, utc_offset):
    try:
        date = dateutil.parser.parse(iso_date)
    except (ValueError, AttributeError):
        return None

    if utc_offset is not None:
        server_utc_offset_in_hours = -float(time.timezone) / 3600 + time.daylight
        delta = datetime.timedelta(hours=(utc_offset - server_utc_offset_in_hours))
        return date + delta

    return date
