# coding=utf-8

import unittest

from hhwebutils import urls


class TestUrls(unittest.TestCase):
    test_data = [
        ('/x.ru', {}, [], '/x.ru'),
        ('/x.ru?123', {}, [], '/x.ru?123='),
        ('/x.ru', {'d': 'r'}, [], '/x.ru?d=r'),
        ('/x.ru?s=e', {}, ['s'], '/x.ru'),
        ('/x.ru?s=e&r=m', {}, ['s'], '/x.ru?r=m'),
        ('y.ru', {}, [], 'y.ru'),
        ('y.ru?id=1', {}, [], 'y.ru?id=1'),
        ('http://y.ru?id=1', {}, [], 'http://y.ru?id=1'),
        ('myapp://y.ru?id=1', {}, [], 'myapp://y.ru?id=1'),
        ('http://y.ru?id=1', {}, ['id'], 'http://y.ru'),
        ('myapp://y.ru?id=1', {}, ['id'], 'myapp://y.ru'),
        ('http://y.ru?id=1', {'x': 'y'}, [], 'http://y.ru?x=y&id=1'),
        ('myapp://y.ru?id=1', {'x': 'y'}, [], 'myapp://y.ru?x=y&id=1'),
        ('http://example.com/path?param=', {'code': '123'}, [], 'http://example.com/path?code=123&param='),
        ('http://example.com/path?param', {'code': '123'}, [], 'http://example.com/path?code=123&param='),
        ('myapp://example.com/path?param', {'code': '123'}, [], 'myapp://example.com/path?code=123&param='),
        ('example.com/path?param', {'code': '123'}, [], 'example.com/path?code=123&param='),
        ('y.ru/test', {}, [], 'y.ru/test'),
        ('y.ru/test?id=1', {}, [], 'y.ru/test?id=1'),
        ('http://y.ru/test?id=1', {}, [], 'http://y.ru/test?id=1'),
        ('myapp://y.ru/test?id=1', {}, [], 'myapp://y.ru/test?id=1'),
        ('http://y.ru/test?id=1', {}, ['id'], 'http://y.ru/test'),
        ('myapp://y.ru/test?id=1', {}, ['id'], 'myapp://y.ru/test'),
        ('http://y.ru/test?id=1', {'x': 'y'}, [], 'http://y.ru/test?x=y&id=1'),
        ('myapp://y.ru/test?id=1', {'x': 'y'}, [], 'myapp://y.ru/test?x=y&id=1'),
        ('http://example.com/path?param', {'code': '123'}, [], 'http://example.com/path?code=123&param='),
        ('http://example.com/path?param1=1#open', {'code': '123'}, [],
         'http://example.com/path?code=123&param1=1#open'),
        ('myapp://example.com/path?param', {'code': '123'}, [], 'myapp://example.com/path?code=123&param='),
        ('example.com/path?param', {'code': '123'}, [], 'example.com/path?code=123&param='),
        ('asdfasdf://', {'code': '123'}, [], 'asdfasdf://?code=123'),
        ('asdfasdf://?param', {'code': '123'}, [], 'asdfasdf://?code=123&param='),
        ('asdfasdf://?param=1', {'code': '123'}, [], 'asdfasdf://?code=123&param=1'),
        ('asdfasdf:///test', {'code': '123'}, [], 'asdfasdf:///test?code=123'),
        ('asdfasdf:///test?param', {'code': '123'}, [], 'asdfasdf:///test?code=123&param='),
        ('asdfasdf:///test?param=1', {'code': '123'}, [], 'asdfasdf:///test?code=123&param=1'),
        ('asdfasdf:///test?param=1', {'code': u'привет'}, [],
         'asdfasdf:///test?code=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82&param=1'),
        ('asdfasdf:///test?param=1', {'code': u'test'.encode('latin1')}, [], 'asdfasdf:///test?code=test&param=1'),
        (u'http://alexey@myapp.ru:8080/path/to/app?key=%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0', {'code': '123'}, [],
         u'http://alexey@myapp.ru:8080/path/to/app?code=123&key=%D0%BC%D0%BE%D1%81%D0%BA%D0%B2%D0%B0'),
    ]

    def test_update_url(self):
        for url, update_args, remove_args, result in self.test_data:
            formatted = urls.update_url(url, update_args, remove_args)
            self.assertEqual(formatted, result)
