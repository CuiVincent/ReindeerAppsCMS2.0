__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.base.base_handler


class AppListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        self.render('cms/page/app/app_list.html')
