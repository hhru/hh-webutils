# coding=utf-8

import logging
import unittest

from hhwebutils.pager import get_paging

logger = logging.getLogger('test_logger')


class TestPageHelpersPaging(unittest.TestCase):
    maxDiff = None

    @staticmethod
    def get_dots_pages(paging):
        return [item.get('page') for item in paging['pages'] if item.get('text') == "..."]

    @staticmethod
    def get_pages_items(paging):
        return [item for item in paging['pages'] if item.get('text') != "..."]

    def assert_selected_page(self, pager, expected_page):
        page = None

        for item in pager:
            if item.get('selected'):
                page = int(item.get('page'))

        self.assertEqual(page, expected_page,
                         'Expected selected page: "{0}", got "{1}"'.format(expected_page, page))

    def test_no_pages(self):
        current_page, paging = get_paging(logger, items_number=10)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging, None)

        current_page, paging = get_paging(logger, items_number=100, items_on_page=100)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging, None)

        current_page, paging = get_paging(logger, items_number=10, current_page=1)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging, None)

        current_page, paging = get_paging(logger, items_number=10, items_on_page=10, current_page=10)
        self.assertEqual(current_page, 0)
        self.assertEqual(paging, None)

    def assert_total_error(self, current_page, paging):
        self.assertEqual(current_page, None)
        self.assertEqual(paging, None)

    def test_bad_items_number(self):
        self.assert_total_error(*get_paging(logger, items_number='100ds'))

    def test_bad_items_on_page(self):
        self.assert_total_error(*get_paging(logger, items_number='100', items_on_page='0s'))

    def test_zero_items_on_page(self):
        self.assert_total_error(*get_paging(logger, items_number='100', items_on_page='0'))

    def test_negative_items_on_page(self):
        self.assert_total_error(*get_paging(logger, items_number='100', items_on_page='-1'))

    def test_bad_total_pages(self):
        current_page, paging_xml = get_paging(logger, total_pages='50abcd')
        self.assertEqual(current_page, None)
        self.assertEqual(paging_xml, None)

    def test_both_total_pages_and_items_number_specified(self):
        with self.assertRaises(TypeError) as cm:
            get_paging(logger, total_pages=10, items_number=20)

        self.assertEqual(str(cm.exception), 'Only one of items_number or total_pages should be specified')

    def test_none_of_total_pages_and_items_number_specified(self):
        with self.assertRaises(TypeError) as cm:
            get_paging(logger)

        self.assertEqual(str(cm.exception), 'Only one of items_number or total_pages should be specified')

    def test_input_params_to_int(self):
        current_page, paging = get_paging(logger, items_number='100', current_page='2', items_on_page='10')
        self.assertEqual(current_page, 2)
        self.assertNotEqual(paging, None)

    def test_selected_page_in_dict(self):
        current_page, paging = get_paging(logger, items_number=100)
        self.assertEqual(current_page, 0)
        self.assert_selected_page(paging.get('pages'), 0)

        current_page, paging = get_paging(logger, items_number=10, items_on_page=3, current_page=100)
        self.assertEqual(current_page, 3)
        self.assert_selected_page(paging.get('pages'), 3)

    def test_pager_items_count(self):
        current_page, paging = get_paging(logger, items_number=101, items_on_page=10)
        self.assertEqual(len(paging['pages']), 11)

        current_page, paging = get_paging(logger, items_number=100, items_on_page=10)
        self.assertEqual(len(paging['pages']), 10)

        current_page, paging = get_paging(logger, items_number=91, items_on_page=10)
        self.assertEqual(len(paging['pages']), 10)

        current_page, paging = get_paging(logger, items_number=95, items_on_page=10)
        self.assertEqual(len(paging['pages']), 10)

    def test_dots(self):
        for cur_page in range(90, 94):
            current_page, paging = get_paging(logger,
                                              items_number=100,
                                              items_on_page=1,
                                              current_page=cur_page,
                                              paging_links_number=10)
            self.assertEqual([cur_page - 10, 99], self.get_dots_pages(paging))

        for cur_page in range(94, 100):
            current_page, paging = get_paging(logger,
                                              items_number=100,
                                              items_on_page=1,
                                              current_page=cur_page,
                                              paging_links_number=10)
            self.assertEqual([cur_page - 10], self.get_dots_pages(paging))

        for cur_page in range(6):
            current_page, paging = get_paging(logger,
                                              items_number=100,
                                              items_on_page=1,
                                              current_page=cur_page,
                                              paging_links_number=10)
            self.assertEqual([cur_page + 10], self.get_dots_pages(paging))

        for cur_page in range(11, 18):
            current_page, paging = get_paging(logger,
                                              items_number=100,
                                              items_on_page=1,
                                              current_page=cur_page,
                                              paging_links_number=10)
            self.assertEqual([cur_page - 10, cur_page + 10], self.get_dots_pages(paging))

    def test_paging_links_limit(self):
        current_page, paging = get_paging(logger,
                                          items_number=100,
                                          items_on_page=1,
                                          current_page=50,
                                          paging_links_number=10)
        self.assertEqual(len(self.get_pages_items(paging)), 11)

        current_page, paging = get_paging(logger,
                                          items_number=100,
                                          items_on_page=1,
                                          current_page=50,
                                          paging_links_number=1)
        self.assertEqual(len(self.get_pages_items(paging)), 1)

        current_page, paging = get_paging(logger,
                                          items_number=100,
                                          items_on_page=1,
                                          current_page=50,
                                          paging_links_number=2)
        self.assertEqual(len(self.get_pages_items(paging)), 3)

        current_page, paging = get_paging(logger,
                                          items_number=100,
                                          items_on_page=1,
                                          current_page=50,
                                          paging_links_number=3)
        self.assertEqual(len(self.get_pages_items(paging)), 3)

    def test_intervals_intersection(self):
        for cur_page in range(6):
            current_page, paging = get_paging(logger, items_number=100, items_on_page=1,
                                              current_page=cur_page, paging_links_number=10)
            self.assertEqual(self.get_pages_items(paging)[0].get('page'), 0)
            self.assertEqual(self.get_pages_items(paging)[-1].get('page'), 10)

        current_page, paging = get_paging(logger, items_number=100, items_on_page=1, current_page=6,
                                          paging_links_number=10)
        self.assertEqual(self.get_pages_items(paging)[0].get('page'), 1)
        self.assertEqual(self.get_pages_items(paging)[-1].get('page'), 11)

        current_page, paging = get_paging(logger, items_number=100, items_on_page=1, current_page=93,
                                          paging_links_number=10)
        self.assertEquals(self.get_pages_items(paging)[0].get('page'), 88)
        self.assertEquals(self.get_pages_items(paging)[-1].get('page'), 99)

        for cur_page in range(94, 100):
            current_page, paging = get_paging(logger, items_number=100, items_on_page=1,
                                              current_page=cur_page, paging_links_number=10)
            self.assertEqual(self.get_pages_items(paging)[0].get('page'), 89)
            self.assertEqual(self.get_pages_items(paging)[-1].get('page'), 99)

    def test_next_previous(self):
        current_page, paging = get_paging(logger, items_number=10, items_on_page=1,
                                          paging_links_number=1, current_page=0)
        self.assertEqual(paging['previous']['disabled'], True)
        self.assertEqual(paging['next']['disabled'], False)

        current_page, paging = get_paging(logger, items_number=10, items_on_page=1,
                                          paging_links_number=1, current_page=1)
        self.assertEqual(paging['previous']['disabled'], False)
        self.assertEqual(paging['next']['disabled'], False)

        current_page, paging = get_paging(logger, items_number=10, items_on_page=1,
                                          paging_links_number=1, current_page=10)
        self.assertEqual(paging['previous']['disabled'], False)
        self.assertEqual(paging['next']['disabled'], True)

    def test_paging(self):
        current_page, paging = get_paging(logger, items_number=10, items_on_page=3, current_page=1)

        expected = {
            'previous': {
                'disabled': False,
                'page': 0
            },
            'pages': [
                {'text': '1', 'page': 0, 'selected': False},
                {'text': '2', 'page': 1, 'selected': True},
                {'text': '3', 'page': 2, 'selected': False},
                {'text': '4', 'page': 3, 'selected': False}

            ],
            'next': {
                'disabled': False,
                'page': 2
            },
            'os': 'Win'
        }
        self.assertDictEqual(expected, paging)
        self.assertEqual(1, current_page)

    def test_paging_with_total_pages(self):
        current_page, paging = get_paging(logger, total_pages=4, items_on_page=3, current_page=3)
        expected = {
            'previous': {
                'disabled': False,
                'page': 2
            },
            'pages': [
                {'text': '1', 'page': 0, 'selected': False},
                {'text': '2', 'page': 1, 'selected': False},
                {'text': '3', 'page': 2, 'selected': False},
                {'text': '4', 'page': 3, 'selected': True}

            ],
            'next': {
                'disabled': True,
                'page': 4
            },
            'os': 'Win'
        }
        self.assertDictEqual(expected, paging)
        self.assertEqual(3, current_page)
