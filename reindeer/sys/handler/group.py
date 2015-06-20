__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys.model.sys_group import SysGroup


class GroupListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        self.render('sys/group/group_list.html')

    def post(self):
        json = SysGroup.get_all_json()
        r_json = '{"success": true, "aaData":'+json+'}'
        print(r_json)
        return self.write(r_json)
