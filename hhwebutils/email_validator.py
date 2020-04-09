import re

_EMAIL_PATTERN = re.compile(r'''^[\!\#\$\%\&\*\+\-\.\/\^\_\`\=\?\{\|\}\~0-9a-zа-яё]+   # Local-part
                                @[\!\#\$\%\&\*\+\-\.\/\^\_\`\=\?\{\|\}\~0-9a-zа-яё]+   # Domain
                                \.[\!\#\$\%\&\*\+\-\.\/\^\_\`\=\?\{\|\}\~0-9a-zа-яё]+$ # TLD''',
                            re.VERBOSE | re.IGNORECASE)


def is_email_valid(email: str) -> bool:
    if not email or len(email) > 256 or not _EMAIL_PATTERN.match(email):
        return False
    return email[-1] != '.'
