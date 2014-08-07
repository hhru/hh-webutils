# coding=utf-8

import unittest
import os
import sys

import pep8


class TestPep8(unittest.TestCase):
    CHECKED_FILES = ('hhwebutils', 'hhwebutils_tests', 'setup.py')

    def test_pep8(self):
        import hhwebutils
        root_dir = os.path.realpath(os.path.join(os.path.dirname(hhwebutils.__file__), '..'))
        sys.stderr.write('hhwebutils root dir: {}\n'.format(root_dir))
        pep8style = pep8.StyleGuide(
            show_pep8=False,
            show_source=True,
            max_line_length=120
        )

        result = pep8style.check_files(map(lambda p: os.path.join(root_dir, p), TestPep8.CHECKED_FILES))
        self.assertEqual(result.total_errors, 0, 'Pep8 found code style errors or warnings')
