# coding=utf-8

import logging
import unittest

from lxml import etree
from lxml_asserts.testcase import LxmlTestCaseMixin

import hhwebutils.pager as ph

logger = logging.getLogger('test_logger')


class TestPageHelpersPaging(LxmlTestCaseMixin, unittest.TestCase):
    def get_dots_pages(self, xml):
        return xml.xpath('item[@text="..."]/@page')

    def get_all_items(self, xml):
        return xml.xpath('item')

    def get_pages_items(self, xml):
        return xml.xpath('item[@text != "..."]')

    def assert_selected_page(self, xml, expected_page):
        try:
            page = int(xml.xpath('item[@selected="true"]/@page')[0])
        except Exception:
            page = None
        self.assertEqual(page, expected_page,
                         'Expected selected page in xml: "{0}", got "{1}"'.format(expected_page, page))

    def test_no_xml(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging_xml, None)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=100)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging_xml, None)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, current_page=1)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging_xml, None)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=10, current_page=10)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging_xml, None)

    def assert_total_error(self, current_page, paging_xml):
        self.assertEqual(current_page, None)
        self.assertEqual(paging_xml, None)

    def test_bad_items_number(self):
        self.assert_total_error(*ph.get_paging_xml(logger, items_number='100ds'))

    def test_bad_items_on_page(self):
        self.assert_total_error(*ph.get_paging_xml(logger, items_number='100', items_on_page='0s'))

    def test_zero_items_on_page(self):
        self.assert_total_error(*ph.get_paging_xml(logger, items_number='100', items_on_page='0'))

    def test_negative_items_on_page(self):
        self.assert_total_error(*ph.get_paging_xml(logger, items_number='100', items_on_page='-1'))

    def test_bad_total_pages(self):
        current_page, paging_xml = ph.get_paging_xml(logger, total_pages='50abcd')
        self.assertEqual(current_page, None)
        self.assertEqual(paging_xml, None)

    def test_both_total_pages_and_items_number_specified(self):
        try:
            ph.get_paging_xml(logger, total_pages=10, items_number=20)
        except TypeError as e:
            self.assertEqual(str(e), 'Only one of items_number or total_pages should be specified')
        else:
            self.fail('TypeError should raised')

    def test_none_of_total_pages_and_items_number_specified(self):
        try:
            ph.get_paging_xml(logger)
        except TypeError:
            pass
        else:
            self.fail('TypeError should raised')

    def test_input_params_to_int(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number='100', current_page='2',
                                                     items_on_page='10')
        self.assertEqual(current_page, 2)
        self.assertNotEqual(paging_xml, None)

    def test_selected_page_in_xml(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100)
        self.assertEqual(current_page, 0)
        self.assert_selected_page(paging_xml, 0)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=3, current_page=10)
        self.assertEqual(current_page, 3)
        self.assert_selected_page(paging_xml, 3)

    def test_pager_items_count(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=101, items_on_page=10)
        self.assertEqual(len(self.get_all_items(paging_xml)), 6)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=10)
        self.assertEqual(len(self.get_all_items(paging_xml)), 6)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=91, items_on_page=10)
        self.assertEqual(len(self.get_all_items(paging_xml)), 6)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=95, items_on_page=10)
        self.assertEqual(len(self.get_all_items(paging_xml)), 6)

    def test_dots(self):
        for cur_page in range(90, 94):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEqual([str(cur_page - 10), '99'], self.get_dots_pages(paging_xml))

        for cur_page in range(94, 100):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEqual([str(cur_page - 10)], self.get_dots_pages(paging_xml))

        for cur_page in range(6):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEqual([str(cur_page + 10)], self.get_dots_pages(paging_xml))

        for cur_page in range(11, 18):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEqual([str(cur_page - 10), str(cur_page + 10)], self.get_dots_pages(paging_xml))

    def test_paging_links_limit(self):
        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=10)
        self.assertEqual(len(self.get_pages_items(paging_xml)), 11)

        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=1)
        self.assertEqual(len(self.get_pages_items(paging_xml)), 1)

        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=2)
        self.assertEqual(len(self.get_pages_items(paging_xml)), 3)

        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=3)
        self.assertEqual(len(self.get_pages_items(paging_xml)), 3)

    def test_intervals_intersection(self):
        for cur_page in range(6):
            current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1,
                                                         current_page=cur_page, paging_links_number=10)
            self.assertEqual(self.get_pages_items(paging_xml)[0].get('page'), '0')
            self.assertEqual(self.get_pages_items(paging_xml)[-1].get('page'), '10')

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1, current_page=6,
                                                     paging_links_number=10)
        self.assertEqual(self.get_pages_items(paging_xml)[0].get('page'), '1')
        self.assertEqual(self.get_pages_items(paging_xml)[-1].get('page'), '11')

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1, current_page=93,
                                                     paging_links_number=10)
        self.assertEquals(self.get_pages_items(paging_xml)[0].get('page'), '88')
        self.assertEquals(self.get_pages_items(paging_xml)[-1].get('page'), '99')

        for cur_page in range(94, 100):
            current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1,
                                                         current_page=cur_page, paging_links_number=10)
            self.assertEqual(self.get_pages_items(paging_xml)[0].get('page'), '89')
            self.assertEqual(self.get_pages_items(paging_xml)[-1].get('page'), '99')

    def test_next_previous(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=1,
                                                     paging_links_number=1, current_page=0)
        self.assertXpathInXml(paging_xml, 'previous[@disabled="True"]')
        self.assertXpathInXml(paging_xml, 'next[@disabled="False"]')

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=1,
                                                     paging_links_number=1, current_page=1)
        self.assertXpathInXml(paging_xml, 'previous[@disabled="False"]')
        self.assertXpathInXml(paging_xml, 'next[@disabled="False"]')

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=1,
                                                     paging_links_number=1, current_page=10)
        self.assertXpathInXml(paging_xml, 'previous[@disabled="False"]')
        self.assertXpathInXml(paging_xml, 'next[@disabled="True"]')

    def test_paging_xml(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=3, current_page=1)
        expected = '''
            <pager>
                <previous disabled="False" page="0"/>
                <item text="1" inShortRange="True" page="0"/>
                <item text="2" inShortRange="True" page="1" selected="true"/>
                <item text="3" inShortRange="True" page="2"/>
                <item text="4" inShortRange="False" page="3"/>
                <next disabled="False" page="2"/>
                <os>Win</os>
            </pager>
            '''.strip()
        self.assertXmlEqual(expected, paging_xml)
        self.assertEqual(1, current_page)

    def test_paging_xml_with_total_pages(self):
        current_page, paging_xml = ph.get_paging_xml(logger, total_pages=4, items_on_page=3, current_page=3)
        expected = '''
            <pager>
                <previous disabled="False" page="2"/>
                <item text="1" inShortRange="False" page="0"/>
                <item text="2" inShortRange="True" page="1"/>
                <item text="3" inShortRange="True" page="2"/>
                <item text="4" inShortRange="True" page="3" selected="true"/>
                <next disabled="True" page="4"/>
                <os>Win</os>
            </pager>
            '''.strip()
        self.assertXmlEqual(expected, paging_xml)
        self.assertEqual(3, current_page)

    def assertXpathInXml(self, xml, xpath):
        nodes = xml.xpath(xpath)
        self.assertNotEqual(
            nodes, [],
            '\n"{0}" have no matches in \n{1}'.format(xpath, etree.tostring(xml, pretty_print=True))
        )
