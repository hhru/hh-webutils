# coding=utf-8

import unittest

import pep8


class TestPep8(unittest.TestCase):
    CHECKED_FILES = ('hhwebutils', 'hhwebutils_tests', 'setup.py')

    def test_pep8(self):
        pep8style = pep8.StyleGuide(
            show_pep8=False,
            show_source=True,
            max_line_length=120
        )

        result = pep8style.check_files(TestPep8.CHECKED_FILES)
        self.assertEqual(result.total_errors, 0, 'Pep8 found code style errors or warnings')
