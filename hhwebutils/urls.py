from collections import Iterable
from collections import Mapping
import types
import urllib
import urlparse


def update_url(url, update_args=None, remove_args=None):

    def deep_encode(data, charset='utf8'):
        if isinstance(data, unicode):
            return data.encode(charset)
        if isinstance(data, Mapping):
            return {key: deep_encode(data[key], charset) for key in data}
        if isinstance(data, Iterable) and not isinstance(data, types.StringTypes):
            return [deep_encode(value, charset) for value in data]
        return data

    scheme, sep, url_new = url.partition('://')
    if len(scheme) == len(url):
        scheme = ''
    else:
        url = '//' + url_new

    url_split = urlparse.urlsplit(url.encode('utf-8') if isinstance(url, unicode) else url)
    query_dict = urlparse.parse_qs(url_split.query, keep_blank_values=True)

    if update_args:
        update_args = deep_encode(update_args, 'utf-8')
        query_dict.update(update_args)

    if remove_args:
        query_dict = {k: query_dict.get(k) for k in query_dict if k not in remove_args}

    query = urllib.urlencode(query_dict, doseq=True)

    # specific case without net location
    # warning: does not preserve original string type
    if not url_split.netloc:
        return ''.join([
            scheme,
            '://' if scheme else '',
            url_split.path,
            '?' if query else '',
            query,
            '#' if url_split.fragment else '',
            url_split.fragment
        ])

    return urlparse.urlunsplit((scheme, url_split.netloc, url_split.path, query, url_split.fragment))
