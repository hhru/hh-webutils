# coding=utf-8
import re
from copy import deepcopy

from lxml import etree

from hhwebutils.compat import unicode_type

__clean_ns_re = re.compile(r'^({.*})(.*)$')

# http://www.w3.org/TR/xml/#charsets
_INVALID_CHARACTERS_REGEXP = re.compile(u'[' +
                                        u'\x00-\x08' +
                                        u'\x0b' +
                                        u'\x0c' +
                                        u'\x0e-\x1F' +
                                        u'\x7f-\x84'
                                        u'\x86-\x9f'
                                        u'\uD800-\uDFFF' +
                                        u'\uFDD0-\uFDEF' +
                                        u'\uFFFE' +
                                        u'\uFFFF]')


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
    parts.extend(etree.tostring(c, encoding='unicode', method=method) for c in node.iterchildren())
    parts = filter(None, parts)
    return u''.join(parts)


def strip_invalid_characters(string):
    if isinstance(string, bytes):
        string = string.decode('utf-8')
    elif not isinstance(string, unicode_type):
        string = unicode_type(string)
    return _INVALID_CHARACTERS_REGEXP.sub(u'', string)
