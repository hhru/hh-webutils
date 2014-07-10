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
