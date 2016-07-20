from collections import Iterable
from collections import Mapping

import urllib
import urlparse


def update_url(url, update_args=None, remove_args=None):
    scheme, sep, url_new = url.partition('://')
    if len(scheme) == len(url):
        scheme = ''
    else:
        url = '//' + url_new

    url_split = urlparse.urlsplit(_to_native_string(url))
    query_dict = urlparse.parse_qs(url_split.query, keep_blank_values=True)

    if update_args:
        update_args = _deep_encode(update_args)
        query_dict.update(update_args)

    if remove_args:
        query_dict = {k: query_dict.get(k) for k in query_dict if k not in remove_args}

    query = urllib.urlencode(query_dict, doseq=True)

    # specific case without net location
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

    return urlparse.urlunsplit(
        [_to_native_string(part) for part in (scheme, url_split.netloc, url_split.path, query, url_split.fragment)]
    )


def _to_native_string(s):
    if isinstance(s, str):
        return s

    if isinstance(s, unicode):
        return s.encode('utf-8')

    return s.decode('utf-8')


def _deep_encode(data):
    if isinstance(data, (bytes, unicode)):
        return _to_native_string(data)

    if isinstance(data, Mapping):
        return {key: _deep_encode(data[key]) for key in data}

    if isinstance(data, Iterable):
        return [_deep_encode(value) for value in data]

    return data
