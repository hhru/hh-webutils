# coding: utf-8
from unittest import TestCase

from hhwebutils.js_validator import is_valid_jsonp_callback_value, is_valid_js_identifier
from hhwebutils.compat import unicode_type


class IsValidJsonpCallbackValue(TestCase):

    def test_good_callback(self):
        self.assertTrue(is_valid_jsonp_callback_value('somevar'))

    def test_bad_callbacks(self):
        for cb in ('function', ' somevar'):
            self.assertFalse(is_valid_jsonp_callback_value(cb))

    def test_nested_level_callback(self):
        self.assertFalse(is_valid_jsonp_callback_value('$.23'))
        self.assertTrue(is_valid_jsonp_callback_value('$.ajaxHandler'))

    def test_array_index_callback(self):
        for cb in ('array_of_functions[42]foo[1]', 'array_of_functions[]', 'array_of_functions["key"]'):
            self.assertFalse(is_valid_jsonp_callback_value(cb))
        for cb in ('array_of_functions[42]', 'array_of_functions[42][1]'):
            self.assertTrue(is_valid_jsonp_callback_value(cb))


class IsValidJsIdentifierTestCase(TestCase):

    def test_valid_identifier(self):
        for val in (u'myfunc', u'Stra\u00dfe', unicode_type(u'привет').encode('utf-8')):
            self.assertTrue(is_valid_js_identifier(val))

    def test_invalid_identifier_unicode_errors(self):
        self.assertFalse(is_valid_js_identifier(unicode_type(u'привет').encode('utf-16')))

    def test_reserved_words(self):
        for val in ('yield', 'for'):
            self.assertFalse(is_valid_js_identifier(val))
