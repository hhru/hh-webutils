from unittest import TestCase

from hhwebutils.email_validator import is_email_valid


class EmailValidatorTestCase(TestCase):
    def test_valid_email(self):
        self.assertTrue(is_email_valid('me@mvx.io'))

    def test_multipart_domain(self):
        self.assertTrue(is_email_valid('me@mail.mvx.io'))

    def test_valid_email_with_numbers(self):
        self.assertTrue(is_email_valid('me1@mvx1.1io'))

    def test_acceptable_digital_email(self):
        self.assertTrue(is_email_valid('1@1.1'))

    def test_acceptable_email(self):
        self.assertTrue(is_email_valid('a@b.c'))

    def test_ignore_case(self):
        self.assertTrue(is_email_valid('Me@Mvx.Io'))

    def test_no_domain(self):
        self.assertFalse(is_email_valid('me@.io'))

    def test_no_tld(self):
        self.assertFalse(is_email_valid('me@mvx.'))

    def test_bad_domain(self):
        self.assertFalse(is_email_valid('me@mvx'))

    def test_no_local_part(self):
        self.assertFalse(is_email_valid('@mvx.io'))

    def test_no_at_sign(self):
        self.assertFalse(is_email_valid('mvx.io'))

    def test_at_sign_and_dot(self):
        self.assertFalse(is_email_valid('@.'))

    def test_none(self):
        self.assertFalse(is_email_valid(None))

    def test_empty(self):
        self.assertFalse(is_email_valid(''))

    def test_blank(self):
        self.assertFalse(is_email_valid(' \t '))

    def test_blank_local_part(self):
        self.assertFalse(is_email_valid(' \t @mvx.io'))

    def test_blank_domain(self):
        self.assertFalse(is_email_valid('me@ \t .io'))

    def test_blank_tld(self):
        self.assertFalse(is_email_valid('me@mvx. \t '))

    def test_local_part_with_bad_symbols(self):
        self.assertFalse(is_email_valid('8(926)850-37-65@mvx.io'))

    def test_domain_with_bad_symbols(self):
        self.assertFalse(is_email_valid('me@m(v)x.io'))

    def test_tld_with_bad_symbols(self):
        self.assertFalse(is_email_valid('me@mvx.i\to'))

    def test_multiple_at_signs(self):
        self.assertFalse(is_email_valid('be@me@mvx.io'))

    def test_multipart_domain_no_tld(self):
        self.assertFalse(is_email_valid('me@mail.mvx.'))

    def test_blank_multipart_domain_and_tld(self):
        self.assertFalse(is_email_valid('me@\t. .io'))

    def test_no_at_sign_and_bad_domain(self):
        self.assertFalse(is_email_valid('hooray'))
