from __future__ import absolute_import
import logging
from autokindle.logging.filters import Filter
from autokindle.logging.handlers import Handler


def getLogger(package, name):
    logger = logging.getLogger(f'{package}.{name}')
    logger.setLevel(logging.DEBUG)
    logger.addFilter(Filter(package, name))
    logger.addHandler(Handler())
    return logger
