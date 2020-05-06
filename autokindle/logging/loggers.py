from __future__ import absolute_import
import logging
from autokindle.logging.filters import Filter


def getLogger(package, name):
    logger = logging.getLogger(f'{package}.{name}')
    logger.addFilter(Filter(package, name))
    return logger
