# -*- coding: utf-8 -*-

import unittest

from lxml import etree


class TestCaseWithXml(unittest.TestCase):

    def assertXpathEquals(self, xml, xpath, result):
        self.assertEqual(xml.xpath(xpath), result)

    def assertXpathNotInXml(self, xml, xpath):
        nodes = xml.xpath(xpath)
        self.assertEqual(nodes, [], '\n"{0}" have matches in \n{1}'.format(xpath,
                                                                           etree.tostring(xml,
                                                                                          pretty_print=True)))

    def assertXpathInXml(self, xml, xpath):
        nodes = xml.xpath(xpath)
        self.assertNotEqual(nodes, [], '\n"{0}" have no matches in \n{1}'.format(xpath,
                                                                                 etree.tostring(xml,
                                                                                                pretty_print=True)))
