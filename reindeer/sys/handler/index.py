__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import tornado.web
import reindeer.base.base_handler


class IndexHandler(reindeer.base.base_handler.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render('sys/main.html')
