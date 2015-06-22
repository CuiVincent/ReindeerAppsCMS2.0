__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys.model.sys_group import SysGroup
from tornado.escape import json_encode


class ActionListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        self.render('sys/page/action/action_list.html')

    def post(self):
        return self.write(json_encode({'success': True}))
