# coding=utf-8

import os
import re


def parse_version_from_changelog(package_name, root_dir):
    try:
        deb_path = os.path.join(root_dir, 'debian/changelog')
        with open(deb_path, 'r') as changelog:
            regmatch = re.match(r'%s \((.*)\).*' % package_name, changelog.readline())
            return regmatch.group(0)
    except (IOError, AttributeError):
        return 'unknown_version'
