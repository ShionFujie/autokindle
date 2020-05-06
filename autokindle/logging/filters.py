from __future__ import absolute_import
import logging


class Filter(logging.Filter):
    def __init__(self, package, name):
        self.package = package
        self.name = name

    def filter(self, record):
        record.package = self.package
        record.simpleName = self.name
        return True
