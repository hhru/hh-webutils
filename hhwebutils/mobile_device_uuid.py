import re

UUID_RE = re.compile('UUID:? ([-\w/+=]+)', re.I)


def parse_uuid(user_agent):
    if user_agent is None:
        return None

    uuid = re.search(UUID_RE, user_agent)
    if uuid is not None:
        return uuid.group(1).upper()
