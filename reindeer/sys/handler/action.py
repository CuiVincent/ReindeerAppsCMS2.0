__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys import constants
from reindeer.sys.model.sys_action import SysAction
from reindeer.sys.exceptions import BusinessRuleException
from tornado.escape import json_encode


class ActionListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        actions = SysAction.get_tree_by_parent(constants.action_root_main_parent, constants.action_type_menu_menu)
        self.render('sys/page/action/action_list.html', actions=actions)

    def post(self):
        id = self.get_argument('id')
        if id:
            return self.write(json_encode({'success': True, 'data': SysAction.get_json_by_id(id)}))
        else:
            raise BusinessRuleException(1151)


class ActionAddHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        name = self.get_argument('name')
        des = self.get_argument('des')
        parent = self.get_argument('pid')
        if not parent:
            parent = constants.action_root_main_parent;
        url = self.get_argument('url')
        sort = self.get_argument('sort')
        icon = self.get_argument('icon')
        err_code = SysAction.add(name=name, url=url, des=des,
                                 parent=parent,
                                 sort=sort, icon=icon)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)