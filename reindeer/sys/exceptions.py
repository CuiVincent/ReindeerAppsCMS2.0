__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import tornado

from reindeer.sys.constants import err_codes


class BusinessRuleException(Exception):
    def __init__(self, err_code):
        self.err_code = err_code

        try:
            self.msg = err_codes[self.err_code][0]
        except KeyError:
            self.msg = err_codes[2][0]
        try:
            self.info = err_codes[self.err_code][1]
        except KeyError:
            self.info = err_codes[2][1]

    def __str__(self):
        message = "BusinessRule [%d - %s] %s" % (self.err_code, self.msg, self.info)
        return message

    def translate(self, locale):
        _ = locale and locale.translate or tornado.locale.get('en_US')
        self.msg = _(self.msg)
        self.info = _(self.info)
        return self