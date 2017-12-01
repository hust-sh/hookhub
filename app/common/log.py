# coding: utf-8

import logging
import common.config as const

_log_dict = {}

formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s')


def logger(name='server'):

    if name not in _log_dict:
        logger = logging.getLogger(name)
        handler = logging.FileHandler('{}/{}.log'.format(const.LOG_DIR, name))
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        _log_dict[name] = logger

    return _log_dict[name]
