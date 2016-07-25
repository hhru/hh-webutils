# coding=utf-8

import sys

PY3 = sys.version_info >= (3,)

if PY3:
    import urllib.parse as urlparse
    from urllib.parse import quote
    from urllib.parse import unquote
    from urllib.parse import urlencode

    unicode_type = str

else:
    from urllib import quote
    from urllib import unquote
    from urllib import urlencode
    import urlparse

    unicode_type = unicode
