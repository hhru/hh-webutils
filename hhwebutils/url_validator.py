# coding=utf-8

from functools import reduce
import re

from hhwebutils.compat import quote, unquote, urlparse, unicode_type

# Check ascii control characters
_invalid_characters = list(map(chr, list(range(ord('\x00'), ord('\x20'))) + [ord('\x7F')]))
quoted = map(quote, _invalid_characters)

INVALID_CHARACTERS_REGEXP = re.compile('[' + ''.join(_invalid_characters) + ']' + '|' + '|'.join(quoted))

# Filter urls starts with javascript: or data:
VALID_SCHEMES = ('http', 'https')


class UrlValidationException(Exception):
    pass


def validate(url, level='error'):
    """
    Validate and try to fix url

    level can take following values:
        error: return None if url is invalid
        validate: try to fix scheme
        filter: remove invaid charecters and fix scheme
    """

    def sanitize_value(url):
        if url is None or not isinstance(url, (bytes, unicode_type)):
            raise UrlValidationException

        return url

    def sanitize_characters(url):
        if INVALID_CHARACTERS_REGEXP.search(url) is not None:
            if level == 'filter':
                return INVALID_CHARACTERS_REGEXP.sub('', url)
            else:
                raise UrlValidationException

        return url

    def sanitize_scheme(url):
        if urlparse.urlsplit(unquote(url)).scheme not in VALID_SCHEMES:
            if level in ('validate', 'filter'):
                parts = urlparse.urlsplit(url)
                url = urlparse.urlunsplit(('', parts.netloc, parts.path, parts.query, parts.fragment))
                return urlparse.urljoin('http:', re.sub('^/*', '//', url))
            else:
                raise UrlValidationException

        return url

    def sanitize_path(url):
        parts = urlparse.urlsplit(unquote(url))

        if parts.hostname is None or parts.hostname == '':
            raise UrlValidationException

        return url

    try:
        validation_functions = (sanitize_value, sanitize_characters, sanitize_scheme, sanitize_path)
        return reduce(lambda url, validator: validator(url), validation_functions, url)
    except (ValueError, UrlValidationException):
        return None
