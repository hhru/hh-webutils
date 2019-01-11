import re

# 01234567-89ab-cdef-0123-456789abcdef
UUID_RE = re.compile(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', re.I)


def parse_uuid(text):
    uuid = re.search(UUID_RE, text)
    if uuid is not None:
        return uuid.group()
