__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys import constants
from reindeer.sys.model.sys_action import SysAction
from reindeer.sys.exceptions import BusinessRuleException
from tornado.escape import json_encode


class ActionListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        self.render('sys/page/action/action_list.html')

    def post(self):
        actions = SysAction.get_ratree_by_parent(constants.action_root_main_parent, constants.action_type_menu_menu)
        return self.write(json_encode({'success': True, 'data': actions}))


class ActionListGroupJoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        actions = SysAction.get_ratree_checked_by_group(
            constants.action_type_menu_menu, gid)
        return self.write(json_encode({'success': True, 'data': actions}))


class ActionAddHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        id = self.get_argument('id')
        action = SysAction.get_json_by_id(id)
        if action:
            return self.write(json_encode({'success': True, 'data': action}))
        else:
            raise BusinessRuleException(1151)

    def post(self):
        name = self.get_argument('name')
        des = self.get_argument('des')
        parent = self.get_argument('pid')
        if not parent:
            parent = constants.action_root_main_parent
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


class ActionDeleteHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        aids = str(self.get_argument('aid')).split(',')
        success_count = 0
        for aid in aids:
            err_code = SysAction.delete(aid)
            if err_code == 0:
                success_count += 1
        if success_count > 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class ActionEditHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        id = self.get_argument('id')
        action = SysAction.get_json_by_id(id)
        if action:
            parent_action = SysAction.get_parent_by_id(id)
            return self.write(json_encode({'success': True, 'data': action,
                                           'parent_data': parent_action and parent_action.NAME or constants.action_root_name}))
        else:
            raise BusinessRuleException(1152)

    def post(self):
        id = self.get_argument('aid')
        name = self.get_argument('name')
        des = self.get_argument('des')
        url = self.get_argument('url')
        sort = self.get_argument('sort')
        icon = self.get_argument('icon')
        err_code = SysAction.update(id=id, name=name, url=url, des=des,
                                    sort=sort, icon=icon)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)