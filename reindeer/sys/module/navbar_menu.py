__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from reindeer.base.base_module import BaseModule


class NavbarMenuModule(BaseModule):
    def render(self, menu_list, level):
        return self.render_string('sys/module/navbar_menu.html', menu_list=menu_list, level=level)


class NavbarScaleMenuModule(BaseModule):
    def render(self, menu_list, level):
        if menu_list['scale_script']:
            try:
                scale_menu_list = eval(str(menu_list['scale_script']))
                if scale_menu_list:
                    return self.render_string('sys/module/navbar_menu.html', menu_list=scale_menu_list, level=level)
            except:
                pass
        return ''