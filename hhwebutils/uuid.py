import re

# 01234567-89ab-cdef-0123-456789abcdef
UUID_RE = re.compile('UUID:? ([0-9a-zA-Z-]+)')


def parse_uuid(text):
    uuid = re.search(UUID_RE, text)
    if uuid is not None:
        return uuid.group(1)
