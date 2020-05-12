from __future__ import absolute_import
import logging

def Handler():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(process)d/%(package)s %(levelname)s/%(simpleName)s: %(message)s',
            '%Y-%m-%d %H:%M:%S'))
        return handler