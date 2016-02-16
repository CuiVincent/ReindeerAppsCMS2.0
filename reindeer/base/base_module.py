__author__ = 'CuiVincent'

import tornado.web


class BaseModule(tornado.web.UIModule):
    def get_current_user(self):
        return self.current_user

    def get_browser_locale(self):
        return self.handler.get_browser_locale()

