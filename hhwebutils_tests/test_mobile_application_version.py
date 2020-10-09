import unittest

from hhwebutils.mobile_application_version import parse_user_agent


class TestUrls(unittest.TestCase):
    def test_ua_parsing_positive(self):
        expected = {
            'ApplicantHH (iPhone 6s; iOS 12.1; Version/4.19.1811.820; UUID 123; ru.hh.iphone)':
                {'platform': 'ios', 'user_platform': 'ios', 'version': '4.19.1811.820', 'app': 'applicant'},

            'by.tut.jobs.android/5.0.2.376, Device: FIG-LX1, Android OS: 8.0.0 (UUID: 123)':
                {'platform': 'android', 'user_platform': 'android', 'version': '5.0.2.376', 'app': 'applicant'},

            'HHApplicant-Live (iPhone 8 Plus; iOS 11.4.1; Version/4.15.1808.732; UUID 123; ru.hh.iphone)':
                {'platform': 'ios', 'user_platform': 'ios', 'version': '4.15.1808.732', 'app': 'applicant'},

            'ApplicantJTB (iPhone 5c; iOS 10.3.1; Version/4.19.1811.471; 123; by.tut.jobs.employee':
                {'platform': 'ios', 'user_platform': 'ios', 'version': '4.19.1811.471', 'app': 'applicant'},

            'ApplicantHHTE (iPhone 6s; iOS 12.0.1; Version/4.19.1811.820; UUID 123; ru.hh.iphone)':
                {'platform': 'ios', 'user_platform': 'ios', 'version': '4.19.1811.820', 'app': 'applicant'},

            'ru.hh.android/4.7.2.344, Device: SM-A520F, Android OS: 8.0.0 (UUID: 123)':
                {'platform': 'android', 'user_platform': 'android', 'version': '4.7.2.344', 'app': 'applicant'},

            'EmployerHH (iPhone 7; iOS 12.1; Version/2.9.1810.352; UUID 123; ru.hh.emp)':
                {'platform': 'ios', 'user_platform': 'ios', 'version': '2.9.1810.352', 'app': 'employer'},

            'HH (iPhone 6s; iOS 11.1.2; Version/2.7.1808.338; UUID F3E29835-A319-4678-83FD-DFD047962A4E; ru.hh.emp)':
                {'platform': 'ios', 'user_platform': 'ios', 'version': '2.7.1808.338', 'app': 'employer'},
        }

        for ua_string, expected_result in expected.items():
            self.assertEqual(parse_user_agent(ua_string), expected_result)

    def test_inconsistent_ua(self):
        self.assertEqual(parse_user_agent(None), None)
        self.assertEqual(parse_user_agent('HH (some version 2.7.1808)'), None)
