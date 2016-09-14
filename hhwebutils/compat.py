# coding=utf-8

import sys

PY3 = sys.version_info >= (3,)

if PY3:
    import urllib.parse as urlparse
    from urllib.parse import quote
    from urllib.parse import unquote
    from urllib.parse import urlencode

    bytes_type = bytes
    unicode_type = str
    unicode_chr = chr

else:
    from urllib import quote
    from urllib import unquote
    from urllib import urlencode
    import urlparse

    bytes_type = str
    unicode_type = unicode
    unicode_chr = unichr
