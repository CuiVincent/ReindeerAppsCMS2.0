__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from reindeer.sys.base_module import BaseModule


class NavbarMenuModule(BaseModule):
    def render(self, menu_list, level):
        return self.render_string('sys/module/navbar_menu.html', menu_list=menu_list, level=level)