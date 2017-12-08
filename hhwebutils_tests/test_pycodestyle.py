# coding=utf-8

import unittest
import os.path

import pycodestyle

from hhwebutils_tests import PROJECT_DIR


class TestPycodestyle(unittest.TestCase):
    CHECKED_FILES = ('hhwebutils', 'hhwebutils_tests', 'setup.py')
    MAX_LINE_LENGTH_EXCLUDED_FILES = ['device_detection_test_data.py']

    def test_pycodestyle(self):
        style_guide = pycodestyle.StyleGuide(
            show_pep8=False,
            show_source=True,
            max_line_length=120,
            ignore=['E731'],
            exclude=TestPycodestyle.MAX_LINE_LENGTH_EXCLUDED_FILES
        )

        result = style_guide.check_files([os.path.join(PROJECT_DIR, p) for p in TestPycodestyle.CHECKED_FILES])
        self.assertEqual(result.total_errors, 0, 'Pycodestyle found code style errors or warnings')
