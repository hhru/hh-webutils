# coding=utf-8

import unittest

from hhwebutils import urls
from hhwebutils.compat import urlparse


class TestUrls(unittest.TestCase):
    test_data = [
        ('/hh.ru', {}, [], '/hh.ru'),
        ('/hh.ru?123', {}, [], '/hh.ru?123='),
        ('/hh.ru', {'d': 'r'}, [], '/hh.ru?d=r'),
        ('/hh.ru?s=e', {}, ['s'], '/hh.ru'),
        ('/hh.ru?s=e&r=m', {}, ['s'], '/hh.ru?r=m'),

        ('hh.ru', {}, [], 'hh.ru'),
        ('hh.ru?id=1', {}, [], 'hh.ru?id=1'),
        ('hh.ru?id=2', {}, ['id'], 'hh.ru'),
        ('hh.ru?id=3', {'x': 'y'}, [], ('hh.ru?x=y&id=3',
                                        'hh.ru?id=3&x=y')),
        ('hh.ru/test', {}, [], 'hh.ru/test'),
        ('hh.ru/test?id=1', {}, [], 'hh.ru/test?id=1'),
        ('hh.ru/test?id=2', {}, ['id'], 'hh.ru/test'),
        ('hh.ru/test?id=3', {'x': 'y'}, [], ('hh.ru/test?x=y&id=3',
                                             'hh.ru/test?id=3&x=y')),

        ('hh.ru:8080', {}, [], 'hh.ru:8080'),
        ('hh.ru:8080?id=1', {}, [], 'hh.ru:8080?id=1'),
        ('hh.ru:8080?id=2', {}, ['id'], 'hh.ru:8080'),
        ('hh.ru:8080?id=3', {'x': 'y'}, [], ('hh.ru:8080?x=y&id=3',
                                             'hh.ru:8080?id=3&x=y')),
        ('hh.ru:8080/test', {}, [], 'hh.ru:8080/test'),
        ('hh.ru:8080/test?id=1', {}, [], 'hh.ru:8080/test?id=1'),
        ('hh.ru:8080/test?id=2', {}, ['id'], 'hh.ru:8080/test'),
        ('hh.ru:8080/test?id=3', {'x': 'y'}, [], ('hh.ru:8080/test?x=y&id=3',
                                                  'hh.ru:8080/test?id=3&x=y')),

        ('//hh.ru', {}, [], '//hh.ru'),
        ('//hh.ru?id=1', {}, [], '//hh.ru?id=1'),
        ('//hh.ru?id=2', {}, ['id'], '//hh.ru'),
        ('//hh.ru?id=3', {'x': 'y'}, [], ('//hh.ru?x=y&id=3',
                                          '//hh.ru?id=3&x=y')),
        ('//hh.ru/test', {}, [], '//hh.ru/test'),
        ('//hh.ru/test?id=1', {}, [], '//hh.ru/test?id=1'),
        ('//hh.ru/test?id=2', {}, ['id'], '//hh.ru/test'),
        ('//hh.ru/test?id=3', {'x': 'y'}, [], ('//hh.ru/test?x=y&id=3',
                                               '//hh.ru/test?id=3&x=y')),

        ('//hh.ru:8080', {}, [], '//hh.ru:8080'),
        ('//hh.ru:8080?id=1', {}, [], '//hh.ru:8080?id=1'),
        ('//hh.ru:8080?id=2', {}, ['id'], '//hh.ru:8080'),
        ('//hh.ru:8080?id=3', {'x': 'y'}, [], ('//hh.ru:8080?x=y&id=3',
                                               '//hh.ru:8080?id=3&x=y')),
        ('//hh.ru:8080/test', {}, [], '//hh.ru:8080/test'),
        ('//hh.ru:8080/test?id=1', {}, [], '//hh.ru:8080/test?id=1'),
        ('//hh.ru:8080/test?id=2', {}, ['id'], '//hh.ru:8080/test'),
        ('//hh.ru:8080/test?id=3', {'x': 'y'}, [], ('//hh.ru:8080/test?x=y&id=3',
                                                    '//hh.ru:8080/test?id=3&x=y')),

        ('http://hh.ru', {}, [], 'http://hh.ru'),
        ('http://hh.ru?id=1', {}, [], 'http://hh.ru?id=1'),
        ('http://hh.ru?id=2', {}, ['id'], 'http://hh.ru'),
        ('http://hh.ru?id=3', {'x': 'y'}, [], ('http://hh.ru?x=y&id=3',
                                               'http://hh.ru?id=3&x=y')),
        ('http://hh.ru/test', {}, [], 'http://hh.ru/test'),
        ('http://hh.ru/test?id=1', {}, [], 'http://hh.ru/test?id=1'),
        ('http://hh.ru/test?id=2', {}, ['id'], 'http://hh.ru/test'),
        ('http://hh.ru/test?id=3', {'x': 'y'}, [], ('http://hh.ru/test?x=y&id=3',
                                                    'http://hh.ru/test?id=3&x=y')),

        ('http://hh.ru:8080', {}, [], 'http://hh.ru:8080'),
        ('http://hh.ru:8080?id=1', {}, [], 'http://hh.ru:8080?id=1'),
        ('http://hh.ru:8080?id=2', {}, ['id'], 'http://hh.ru:8080'),
        ('http://hh.ru:8080?id=3', {'x': 'y'}, [], ('http://hh.ru:8080?x=y&id=3',
                                                    'http://hh.ru:8080?id=3&x=y')),
        ('http://hh.ru:8080/test', {}, [], 'http://hh.ru:8080/test'),
        ('http://hh.ru:8080/test?id=1', {}, [], 'http://hh.ru:8080/test?id=1'),
        ('http://hh.ru:8080/test?id=2', {}, ['id'], 'http://hh.ru:8080/test'),
        ('http://hh.ru:8080/test?id=3', {'x': 'y'}, [], ('http://hh.ru:8080/test?x=y&id=3',
                                                         'http://hh.ru:8080/test?id=3&x=y')),

        ('magic://hh.ru', {}, [], 'magic://hh.ru'),
        ('magic://hh.ru?id=1', {}, [], 'magic://hh.ru?id=1'),
        ('magic://hh.ru?id=2', {}, ['id'], 'magic://hh.ru'),
        ('magic://hh.ru?id=3', {'x': 'y'}, [], ('magic://hh.ru?x=y&id=3',
                                                'magic://hh.ru?id=3&x=y')),
        ('magic://hh.ru/test', {}, [], 'magic://hh.ru/test'),
        ('magic://hh.ru/test?id=1', {}, [], 'magic://hh.ru/test?id=1'),
        ('magic://hh.ru/test?id=2', {}, ['id'], 'magic://hh.ru/test'),
        ('magic://hh.ru/test?id=3', {'x': 'y'}, [], ('magic://hh.ru/test?x=y&id=3',
                                                     'magic://hh.ru/test?id=3&x=y')),

        ('magic://hh.ru:8080', {}, [], 'magic://hh.ru:8080'),
        ('magic://hh.ru:8080?id=1', {}, [], 'magic://hh.ru:8080?id=1'),
        ('magic://hh.ru:8080?id=2', {}, ['id'], 'magic://hh.ru:8080'),
        ('magic://hh.ru:8080?id=3', {'x': 'y'}, [], ('magic://hh.ru:8080?x=y&id=3',
                                                     'magic://hh.ru:8080?id=3&x=y')),
        ('magic://hh.ru:8080/test', {}, [], 'magic://hh.ru:8080/test'),
        ('magic://hh.ru:8080/test?id=1', {}, [], 'magic://hh.ru:8080/test?id=1'),
        ('magic://hh.ru:8080/test?id=2', {}, ['id'], 'magic://hh.ru:8080/test'),
        ('magic://hh.ru:8080/test?id=3', {'x': 'y'}, [], ('magic://hh.ru:8080/test?x=y&id=3',
                                                          'magic://hh.ru:8080/test?id=3&x=y')),

        ('file:///', {}, [], 'file:///'),
        ('file:///?id=1', {}, [], 'file:///?id=1'),
        ('file:///?id=2', {}, ['id'], 'file:///'),
        ('file:///?id=3', {'x': 'y'}, [], ('file:///?x=y&id=3',
                                           'file:///?id=3&x=y')),
        ('file:///test', {}, [], 'file:///test'),
        ('file:///test?id=1', {}, [], 'file:///test?id=1'),
        ('file:///test?id=2', {}, ['id'], 'file:///test'),
        ('file:///test?id=3', {'x': 'y'}, [], ('file:///test?x=y&id=3',
                                               'file:///test?id=3&x=y')),

        ('custom:///', {}, [], 'custom:///'),
        ('custom:///?id=1', {}, [], 'custom:///?id=1'),
        ('custom:///?id=2', {}, ['id'], 'custom:///'),
        ('custom:///?id=3', {'x': 'y'}, [], ('custom:///?x=y&id=3',
                                             'custom:///?id=3&x=y')),
        ('custom:///test', {}, [], 'custom:///test'),
        ('custom:///test?id=1', {}, [], 'custom:///test?id=1'),
        ('custom:///test?id=2', {}, ['id'], 'custom:///test'),
        ('custom:///test?id=3', {'x': 'y'}, [], ('custom:///test?x=y&id=3',
                                                 'custom:///test?id=3&x=y')),

        ('http://example.com/path?param=', {'code': '123'}, [], ('http://example.com/path?code=123&param=',
                                                                 'http://example.com/path?param=&code=123')),
        ('http://example.com/path?param', {'code': '123'}, [], ('http://example.com/path?code=123&param=',
                                                                'http://example.com/path?param=&code=123')),
        ('http://example.com/path?param=1', {'code': u'привет'}, [],
         ('http://example.com/path?code=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82&param=1',
          'http://example.com/path?param=1&code=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82')),
        (u'http://example.com/привет=abc?param=1', {}, [], 'http://example.com/привет=abc?param=1'),
        ('http://example.com/path?param=1', {'code': u'test'.encode('latin1')}, [],
         ('http://example.com/path?code=test&param=1',
          'http://example.com/path?param=1&code=test')),
        ('http://example.com/path?param1=1#open', {'code': '123'}, [],
         ('http://example.com/path?code=123&param1=1#open',
          'http://example.com/path?param1=1&code=123#open')),
        ('example.com/path?param', {'code': '123'}, [], ('example.com/path?code=123&param=',
                                                         'example.com/path?param=&code=123')),
        ('example.com:8080/path?param', {'code': '123'}, [], ('example.com:8080/path?code=123&param=',
                                                              'example.com:8080/path?param=&code=123')),
        (u'http://alexey@myapp.ru:8080/path/to/app?key=привет', {'code': '123'}, [],
         ('http://alexey@myapp.ru:8080/path/to/app?code=123&key=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82',
          'http://alexey@myapp.ru:8080/path/to/app?key=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82&code=123')),
    ]

    def test_update_url(self):
        for url, update_args, remove_args, result in self.test_data:
            formatted_url = urls.update_url(url, update_args, remove_args)

            if isinstance(result, tuple):
                self.assertIn(formatted_url, result)
            else:
                self.assertEqual(formatted_url, result)

            updated_url = urlparse.urlsplit(formatted_url)
            result_url = urlparse.urlsplit(result[0] if isinstance(result, tuple) else result)

            self.assertEqual(updated_url.scheme, result_url.scheme)
            self.assertEqual(updated_url.netloc, result_url.netloc)
            self.assertEqual(updated_url.path, result_url.path)
            self.assertEqual(urlparse.parse_qs(updated_url.query), urlparse.parse_qs(result_url.query))
            self.assertEqual(updated_url.fragment, result_url.fragment)
