# coding=utf-8

from functools import partial
import logging
import os
import unittest

from hhwebutils.configs import execute_configs, parse_configs

TESTS_DIR = os.path.dirname(__file__)
CFG_PATH = os.path.join(TESTS_DIR, 'test_configs')
DEV_CONFIGS = ['dev.cfg.example', 'dev.cfg']
PROD_CONFIGS = ['prod.cfg']

logger = logging.getLogger('test_logger')


def get_configs_path(configs):
    return map(partial(os.path.join, CFG_PATH), configs)


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


class TestConfigsNew(unittest.TestCase):
    def test_only_dev_configs(self):
        globals_ = {}
        main_configs = get_configs_path(['dev.cfg.example'])
        overrides = get_configs_path(['dev.cfg'])

        configs = parse_configs(main_configs, overrides, logger, globals_, globals_)

        self.assertEqual(configs, get_configs_path(['dev.cfg.example', 'dev.cfg']))
        self.assertFalse(globals_['feature2'])

    def test_prod_configs(self):
        globals_ = {}
        main_configs = get_configs_path(['test_configs_not_exists', 'prod.cfg'])
        overrides = get_configs_path(['test_configs_overrides_not_exists'])

        configs = parse_configs(main_configs, overrides, logger, globals_, globals_)

        self.assertEqual(configs, get_configs_path(['prod.cfg']))
        self.assertTrue(globals_['feature'])

    def test_mix(self):
        globals_ = {}
        main_configs = get_configs_path(['dev.cfg.example', 'prod.cfg'])
        overrides = get_configs_path(['dev.cfg'])

        configs = parse_configs(main_configs, overrides, logger, globals_, globals_)

        self.assertEqual(configs, get_configs_path(['dev.cfg.example', 'dev.cfg']))
        self.assertTrue(globals_['feature1'])
        self.assertFalse(globals_['feature2'])

    def test_no_configs(self):
        main_configs = get_configs_path(['test_configs_not_exists'])
        self.assertRaises(Exception, execute_configs, main_configs, [], logger, {}, {})
