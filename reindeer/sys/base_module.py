__author__ = 'CuiVincent'

import tornado.web


class BaseModule(tornado.web.UIModule):
    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        return user_id


