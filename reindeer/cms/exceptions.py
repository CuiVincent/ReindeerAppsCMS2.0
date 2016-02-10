__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from reindeer.sys.exceptions import BusinessRuleException
from reindeer.cms.constants import cms_err_codes


class CmsBusinessRuleException(BusinessRuleException):
    def __init__(self, err_code):
        self.err_code = err_code
        try:
            self.msg = cms_err_codes[self.err_code][0]
        except KeyError:
            self.msg = cms_err_codes[2][0]
        try:
            self.info = cms_err_codes[self.err_code][1]
        except KeyError:
            self.info = cms_err_codes[2][1]

    def __str__(self):
        message = "CmsBusinessRule [%d - %s] %s" % (self.err_code, self.msg, self.info)
        return message
