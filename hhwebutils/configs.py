# coding=utf-8

import os


def execute_configs(development_configs, production_configs, logger, globals_, locals_):

    def _execute_config(config_file):
        logger.info('executing application config file at {}'.format(config_file))
        execfile(config_file, globals_, locals_)

    has_dev_configs = any(map(os.path.exists, development_configs))

    if not has_dev_configs:
        has_prod_configs = any(map(os.path.exists, production_configs))
        if not has_prod_configs:
            raise Exception('No suitable config files found (tried {}, {})'.format(
                development_configs, production_configs))

    configs = development_configs if has_dev_configs else production_configs
    for cfg in configs:
        if os.path.exists(cfg):
            _execute_config(cfg)

    return configs


def parse_configs(main_configs, overrides, logger, globals_, locals_):
    find_existing = lambda paths: list(filter(os.path.exists, paths))

    def _execute_config(config_file):
        logger.info('executing application config file at {}'.format(config_file))
        execfile(config_file, globals_, locals_)

    configs_main = find_existing(main_configs)
    configs_overrides = find_existing(overrides)

    if not configs_main:
        raise Exception('No suitable config files found (tried {})'.format(main_configs))

    configs = configs_main[:1]
    configs.extend(configs_overrides)

    for cfg in configs:
        _execute_config(cfg)

    return configs
