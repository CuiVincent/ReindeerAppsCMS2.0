__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from reindeer.sys.base_module import BaseModule

from reindeer.sys.model.sys_action import SysAction
from reindeer.sys import constants


class MainMenuModule(BaseModule):
    def render(self, main_menu):
        return self.render_string('sys/module/main_menu.html', main_menu=main_menu)