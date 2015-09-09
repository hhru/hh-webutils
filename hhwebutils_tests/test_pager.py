# -*- coding: utf-8 -*-

from common import TestCaseWithXml
import logging

logger = logging.getLogger('test_logger')

from frontik.testing.xml_asserts import XmlTestCaseMixin

import hhwebutils.pager as ph


class TestPageHelpersPaging(TestCaseWithXml, XmlTestCaseMixin):
    def get_dots_pages(self, xml):
        return xml.xpath('item[@text="..."]/@page')

    def get_all_items(self, xml):
        return xml.xpath('item')

    def get_pages_items(self, xml):
        return xml.xpath('item[@text != "..."]')

    def assert_selected_page(self, xml, expected_page):
        try:
            page = int(xml.xpath('item[@selected="true"]/@page')[0])
        except:
            page = None
        self.assertEquals(page, expected_page,
                          'Expected selected page in xml: "{0}", got "{1}"'.format(expected_page, page))

    def test_no_xml(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10)
        self.assertEquals(current_page, 0)
        self.assertEquals(paging_xml, None)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=100)
        self.assertEquals(current_page, 0)
        self.assertEquals(paging_xml, None)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, current_page=1)
        self.assertEquals(current_page, 0)
        self.assertEquals(paging_xml, None)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=10, current_page=10)
        self.assertEquals(current_page, 0)
        self.assertEquals(paging_xml, None)

    def assert_total_error(self, current_page, paging_xml):
        self.assertEquals(current_page, None)
        self.assertEquals(paging_xml, None)

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
        self.assertEquals(current_page, None)
        self.assertEquals(paging_xml, None)

    def test_both_total_pages_and_items_number_specified(self):
        try:
            ph.get_paging_xml(logger, total_pages=10, items_number=20)
        except TypeError as e:
            self.assertEquals(str(e), 'Only one of items_number or total_pages should be specified')
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
        self.assertEquals(current_page, 2)
        self.assertNotEquals(paging_xml, None)

    def test_selected_page_in_xml(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100)
        self.assertEquals(current_page, 0)
        self.assert_selected_page(paging_xml, 0)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=10, items_on_page=3, current_page=10)
        self.assertEquals(current_page, 3)
        self.assert_selected_page(paging_xml, 3)

    def test_pager_items_count(self):
        current_page, paging_xml = ph.get_paging_xml(logger, items_number=101, items_on_page=10)
        self.assertEquals(len(self.get_all_items(paging_xml)), 11)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=10)
        self.assertEquals(len(self.get_all_items(paging_xml)), 10)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=91, items_on_page=10)
        self.assertEquals(len(self.get_all_items(paging_xml)), 10)

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=95, items_on_page=10)
        self.assertEquals(len(self.get_all_items(paging_xml)), 10)

    def test_dots(self):
        for cur_page in xrange(90, 94):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEquals([str(cur_page-10), '99'], self.get_dots_pages(paging_xml))

        for cur_page in xrange(94, 100):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEquals([str(cur_page-10)], self.get_dots_pages(paging_xml))

        for cur_page in xrange(6):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEquals([str(cur_page + 10)], self.get_dots_pages(paging_xml))

        for cur_page in xrange(11, 18):
            current_page, paging_xml = ph.get_paging_xml(logger,
                                                         items_number=100,
                                                         items_on_page=1,
                                                         current_page=cur_page,
                                                         paging_links_number=10)
            self.assertEquals([str(cur_page-10), str(cur_page + 10)], self.get_dots_pages(paging_xml))

    def test_paging_links_limit(self):
        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=10)
        self.assertEquals(len(self.get_pages_items(paging_xml)), 11)

        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=1)
        self.assertEquals(len(self.get_pages_items(paging_xml)), 1)

        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=2)
        self.assertEquals(len(self.get_pages_items(paging_xml)), 3)

        current_page, paging_xml = ph.get_paging_xml(logger,
                                                     items_number=100,
                                                     items_on_page=1,
                                                     current_page=50,
                                                     paging_links_number=3)
        self.assertEquals(len(self.get_pages_items(paging_xml)), 3)

    def test_intervals_intersection(self):
        for cur_page in xrange(6):
            current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1,
                                                         current_page=cur_page, paging_links_number=10)
            self.assertEquals(self.get_pages_items(paging_xml)[0].get('page'), '0')
            self.assertEquals(self.get_pages_items(paging_xml)[-1].get('page'), '10')

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1, current_page=6,
                                                     paging_links_number=10)
        self.assertEquals(self.get_pages_items(paging_xml)[0].get('page'), '1')
        self.assertEquals(self.get_pages_items(paging_xml)[-1].get('page'), '11')

        current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1, current_page=93,
                                                     paging_links_number=10)
        self.assertEquals(self.get_pages_items(paging_xml)[0].get('page'), '88')
        self.assertEquals(self.get_pages_items(paging_xml)[-1].get('page'), '98')

        for cur_page in xrange(94, 100):
            current_page, paging_xml = ph.get_paging_xml(logger, items_number=100, items_on_page=1,
                                                         current_page=cur_page, paging_links_number=10)
            self.assertEquals(self.get_pages_items(paging_xml)[0].get('page'), '89')
            self.assertEquals(self.get_pages_items(paging_xml)[-1].get('page'), '99')

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
                <item text="1" page="0"/>
                <item text="2" page="1" selected="true"/>
                <item text="3" page="2"/>
                <item text="4" page="3"/>
                <next disabled="False" page="2"/>
                <os>Win</os>
            </pager>
            '''.strip()
        self.assertXmlEqual(expected, paging_xml)
        self.assertEquals(1, current_page)

    def test_paging_xml_with_total_pages(self):
        current_page, paging_xml = ph.get_paging_xml(logger, total_pages=4, items_on_page=3, current_page=3)
        expected = '''
            <pager>
                <previous disabled="False" page="2"/>
                <item text="1" page="0"/>
                <item text="2" page="1"/>
                <item text="3" page="2"/>
                <item text="4" page="3" selected="true"/>
                <next disabled="True" page="4"/>
                <os>Win</os>
            </pager>
            '''.strip()
        self.assertXmlEqual(expected, paging_xml)
        self.assertEquals(3, current_page)
