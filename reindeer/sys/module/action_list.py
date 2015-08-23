__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from reindeer.sys.base_module import BaseModule


class ActionListModule(BaseModule):
    def render(self, actions, checkable, operatable):
        return self.render_string('sys/module/action_list.html', actions=actions, checkable=checkable,
                                  operatable=operatable)