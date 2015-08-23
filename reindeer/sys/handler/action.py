__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys import constants
from reindeer.sys.model.sys_action import SysAction


class ActionListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        actions = SysAction.get_tree_by_parent(constants.action_root_main_parent, constants.action_type_menu_menu)
        self.render('sys/page/action/action_list.html', actions=actions)
