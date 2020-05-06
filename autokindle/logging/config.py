from __future__ import absolute_import
import logging

def setupLogging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(process)d/%(package)s %(levelname)s/%(simpleName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )