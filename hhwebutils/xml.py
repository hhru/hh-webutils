# coding=utf-8
import re
from copy import deepcopy

from lxml import etree

__clean_ns_re = re.compile(r'^({.*})(.*)$')


def xml_to_string(node, clean_xmlns=False, method='xml'):
    if clean_xmlns:
        node = deepcopy(node)
        # remove all namespaces
        for elem in node.iter(tag=etree.Element):
            if elem.tag.startswith('{'):
                elem.tag = __clean_ns_re.sub(r'\2', elem.tag)
        # then clean unused namespaces
        etree.cleanup_namespaces(node)
    parts = [node.text]
    parts.extend(etree.tostring(c, encoding=unicode, method=method) for c in node.iterchildren())
    parts = filter(None, parts)
    return u''.join(parts)
