# coding=utf-8

import os

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.test import test

from hhwebutils import version


class BuildHook(build_py):
    def run(self):
        build_py.run(self)

        build_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.build_lib, 'hhwebutils')
        with open(os.path.join(build_dir, 'version.py'), 'w') as version_file:
            version_file.write('version = "{0}"\n'.format(version))


class TestHook(test):
    def run_tests(self):
        import nose
        nose.main(argv=['nosetests', 'hhwebutils_tests/', '-v'])


setup(
    name='hhwebutils',
    version=__import__('hhwebutils').__version__,
    description='hh.ru python common web utility library',
    long_description=open('README.md').read(),
    url='https://github.com/hhru/hh-webutils',
    cmdclass={'build_py': BuildHook, 'test': TestHook},
    packages=find_packages(exclude=['hhwebutils_tests']),
    install_requires=[
        'lxml >= 2.2.4',
    ],
    test_suite='hhwebutils_tests',
    tests_require=[
        'nose',
        'lxml-asserts',
        'pycodestyle == 2.0.0'
    ],
    zip_safe=False
)
