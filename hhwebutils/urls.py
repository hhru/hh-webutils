# coding=utf-8

from collections import Iterable
from collections import Mapping

import urllib

from hhwebutils.compat import unicode_type, urlencode, urlparse


def update_url(url, update_args=None, remove_args=None):

    # Определяем схему и обрабатываем её вручную, в урле оставляем `//`.
    # Нужно для работы с кастомными схемами (`magic://`) в 2.7.3, см. баг:
    # http://bugs.python.org/issue9374 (исправлен в 2.7.4)
    scheme, sep, url_new = url.partition('://')
    trim_fake_slashes = False

    if len(scheme) == len(url):
        scheme = ''
        if not url.startswith('//'):
            trim_fake_slashes = True
            url = '//' + url
    else:
        url = '//' + url_new

    url_split = urlparse.urlsplit(_to_native_string(url))
    query_dict = urlparse.parse_qs(url_split.query, keep_blank_values=True)

    if update_args:
        update_args = _deep_encode(update_args)
        query_dict.update(update_args)

    if remove_args:
        query_dict = {k: query_dict.get(k) for k in query_dict if k not in remove_args}

    query = urlencode(query_dict, doseq=True)

    # Нужно для работы с кастомными схемами без netloc, см. баг:
    # http://bugs.python.org/issue8339 (wont fix).
    # warning: does not preserve original string type
    if not url_split.netloc:
        return ''.join([
            _to_native_string(scheme),
            '://' if scheme else '',
            url_split.path,
            '?' if query else '',
            _to_native_string(query),
            '#' if url_split.fragment else '',
            _to_native_string(url_split.fragment)
        ])

    result = urlparse.urlunsplit(
        [_to_native_string(part) for part in (scheme, url_split.netloc, url_split.path, query, url_split.fragment)]
    )

    # Убираем слеши, добавленные выше, если `urlunsplit` не убрал их сам.
    if trim_fake_slashes and result.startswith('//'):
        result = result[2:]

    return result


def _to_native_string(s):
    if isinstance(s, str):
        return s

    if isinstance(s, unicode_type):
        return s.encode('utf-8')

    return s.decode('utf-8')


def _deep_encode(data):
    if isinstance(data, (bytes, unicode_type)):
        return _to_native_string(data)

    if isinstance(data, Mapping):
        return {key: _deep_encode(data[key]) for key in data}

    if isinstance(data, Iterable):
        return [_deep_encode(value) for value in data]

    return data
