import re

# 01234567-89ab-cdef-0123-456789abcdef
UUID_RE = re.compile('UUID:? ([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', re.I)


def parse_uuid(user_agent):
    if user_agent is None:
        return None

    uuid = re.search(UUID_RE, user_agent)
    if uuid is not None:
        return uuid.group(1).upper()
