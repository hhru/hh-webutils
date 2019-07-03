# coding=utf-8

import re

from hhwebutils.compat import quote, unquote, urlparse, unicode_type

# Check ascii control characters
_invalid_characters = list(map(chr, list(range(ord('\x00'), ord('\x20'))) + [ord('\x7F')]))
quoted = map(quote, _invalid_characters)

INVALID_CHARACTERS_REGEXP = re.compile('[' + ''.join(_invalid_characters) + ']' + '|' + '|'.join(quoted) + '|;| ')
HOST_PRIMITIVE_REGEXP = re.compile('^.+\..{1,}$')
# Filter urls starts with javascript: or data:
VALID_SCHEMES = ('http', 'https')


def validate(url, level='error'):
    """
    Validate and try to fix url
    Url can lead to any host

    level can take following values:
        error: return None if url is invalid
        validate: try to fix scheme
        filter: remove invalid characters and fix scheme
    """
    return _validate(url, level)


def validate_backurl(backurl, permitted_hosts, permitted_schemes, fallback='/'):
    """
    Validate and try to fix backurl
    Backurl can be relative
    otherwise must lead to permitted host or permitted scheme
    """

    return _validate(
        backurl,
        fallback=fallback,
        default_scheme='https',
        permitted_hosts=permitted_hosts,
        permitted_schemes=permitted_schemes,
        allow_relative_urls=True
    )


def is_permitted_scheme(url, permitted_schemes):
    """
    Check if url leads to permitted scheme
    """
    if not url:
        return False

    return urlparse.urlsplit(unquote(url)).scheme in permitted_schemes


def _validate(
        url,
        level='error',
        fallback=None,
        default_scheme='http',
        permitted_hosts=None,
        permitted_schemes=None,
        allow_relative_urls=False):

    def sanitize_value(url):
        if not url or not isinstance(url, (bytes, unicode_type)):
            return fallback

        return sanitize_characters(url)

    def sanitize_characters(url):
        if INVALID_CHARACTERS_REGEXP.search(url) is not None:
            if level == 'filter':
                return sanitize_scheme(INVALID_CHARACTERS_REGEXP.sub('', url))
            else:
                return fallback

        return sanitize_scheme(url)

    def is_local_url(url):
        # https://docs.microsoft.com/en-us/aspnet/mvc/overview/security/preventing-open-redirection-attacks
        url = unquote(url)
        return (
            url[0] == '/' and (len(url) == 1 or (url[1] not in ('/', '\\')))
        )

    def sanitize_scheme(url):
        if permitted_schemes is not None and is_permitted_scheme(url, permitted_schemes):
            return url

        scheme = urlparse.urlsplit(unquote(url)).scheme
        if not scheme and allow_relative_urls:
            return url if is_local_url(url) else fallback
        if scheme not in VALID_SCHEMES:
            if level in ('validate', 'filter'):
                parts = urlparse.urlsplit(url)
                url = urlparse.urlunsplit(('', parts.netloc, parts.path, parts.query, parts.fragment))
                return sanitize_path(urlparse.urljoin('{}:'.format(default_scheme), re.sub('^/*', '//', url)))
            else:
                return fallback

        return sanitize_path(url)

    def sanitize_path(url):
        parts = urlparse.urlsplit(unquote(url))
        host = parts.netloc
        if not parts.hostname or '\\' in host or not HOST_PRIMITIVE_REGEXP.match(host):
            return fallback

        if permitted_hosts is not None:
            if not any(host_matches(host, valid_host) for valid_host in permitted_hosts):
                return fallback

        return url

    def host_matches(host, valid_host):
        return host == valid_host or host.endswith('.' + valid_host)

    try:
        return sanitize_value(url)
    except ValueError:
        return None
