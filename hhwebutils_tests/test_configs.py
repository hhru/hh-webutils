# coding=utf-8

import logging
import os
import unittest

from hhwebutils.configs import parse_configs

TESTS_DIR = os.path.dirname(__file__)
CFG_PATH = os.path.join(TESTS_DIR, 'test_configs')
DEV_CONFIGS = ['dev.cfg.example', 'dev.cfg']
PROD_CONFIGS = ['prod.cfg']

logger = logging.getLogger('test_logger')


def get_configs_path(configs):
    return [os.path.join(CFG_PATH, cfg) for cfg in configs]


class TestConfigs(unittest.TestCase):
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
        self.assertRaises(Exception, parse_configs, main_configs, [], logger, {}, {})
