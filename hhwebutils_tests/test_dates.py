import datetime
import time
import unittest

from hhwebutils import dates


class TestDates(unittest.TestCase):
    def test_add_utc_offset_to_iso_date(self):
        now = datetime.datetime(1985, 10, 25, 8, 25)  # '1985-10-25 08:25'
        server_utc_offset = -time.timezone / 3600

        self.assertEqual(dates.add_client_utc_offset_to_server_iso_date('1985-10-25 08:25', server_utc_offset), now)
        self.assertEqual(dates.add_client_utc_offset_to_server_iso_date('1985-10-25 08:25', None), now)
        self.assertIsNone(dates.add_client_utc_offset_to_server_iso_date('1985-10--25 08:25', None))
