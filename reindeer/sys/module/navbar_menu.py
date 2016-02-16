__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer
from reindeer.sys import constants
from reindeer.sys.model.sys_action import SysAction
from reindeer.base.base_module import BaseModule


class NavbarMenuModule(BaseModule):
    @reindeer.base.base_handler.authenticated
    def render(self, menu_list, level):
        if level == 0 and not menu_list:
            menu_list = self.get_user_main_menu()
        return self.render_string('sys/module/navbar_menu.html', menu_list=menu_list, level=level)

    def get_user_main_menu(self):
        user_id = self.get_current_user().ID
        menu = SysAction.get_tree_by_user_and_parent(user_id, constants.action_root_main_parent)
        return menu


class NavbarScaleMenuModule(NavbarMenuModule):
    @reindeer.base.base_handler.authenticated
    def render(self, menu_list, level):
        if level == 0 and not menu_list:
            menu_list = self.get_user_main_menu()
        if menu_list['scale_script']:
            try:
                scale_menu_list = eval(str(menu_list['scale_script']))
                if scale_menu_list:
                    return self.render_string('sys/module/navbar_menu.html', menu_list=scale_menu_list, level=level)
            except:
                pass
        return ''
