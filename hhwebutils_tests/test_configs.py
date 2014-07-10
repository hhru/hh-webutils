# coding=utf-8

from functools import partial
import logging
import os
import unittest

from hhwebutils.configs import execute_configs

TESTS_DIR = os.path.dirname(__file__)
DEV_CONFIGS = ['dev.cfg.example', 'dev.cfg']
PROD_CONFIGS = ['prod.cfg']

logger = logging.getLogger('test_logger')


class TestConfigs(unittest.TestCase):
    def test_dev_configs_one_file(self):
        globals_ = {}
        cfg_path = os.path.join(TESTS_DIR, 'test_configs')
        dev_configs = map(partial(os.path.join, cfg_path), [DEV_CONFIGS[0]])
        prod_configs = map(partial(os.path.join, cfg_path), PROD_CONFIGS)

        configs = execute_configs(dev_configs, prod_configs, logger, globals_, globals_)

        self.assertEqual(configs, dev_configs)
        self.assertTrue(globals_['feature2'])

    def test_dev_configs_override(self):
        globals_ = {}
        cfg_path = os.path.join(TESTS_DIR, 'test_configs')
        dev_configs = map(partial(os.path.join, cfg_path), DEV_CONFIGS)
        prod_configs = map(partial(os.path.join, cfg_path), PROD_CONFIGS)

        configs = execute_configs(dev_configs, prod_configs, logger, globals_, globals_)

        self.assertEqual(configs, dev_configs)
        self.assertTrue(globals_['feature1'])
        self.assertFalse(globals_['feature2'])

    def test_prod_configs(self):
        globals_ = {}
        dev_configs = map(partial(os.path.join, TESTS_DIR, 'test_configs_not_exists'), DEV_CONFIGS)
        prod_configs = map(partial(os.path.join, TESTS_DIR, 'test_configs'), PROD_CONFIGS)

        configs = execute_configs(dev_configs, prod_configs, logger, globals_, globals_)

        self.assertEqual(configs, prod_configs)
        self.assertTrue(globals_['feature'])

    def test_no_configs(self):
        cfg_path = os.path.join(TESTS_DIR, 'test_configs_not_exists')
        dev_configs = map(partial(os.path.join, cfg_path), DEV_CONFIGS)
        prod_configs = map(partial(os.path.join, cfg_path), PROD_CONFIGS)

        self.assertRaises(Exception, execute_configs, dev_configs, prod_configs, logger, {}, {})
