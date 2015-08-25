__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys.model.sys_group import SysGroup
from reindeer.sys.exceptions import BusinessRuleException
from tornado.escape import json_encode
from reindeer.sys.model.sys_group_action import SysGroupAction
from reindeer.sys.model.sys_group_user import SysGroupUser

class GroupListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        self.render('sys/page/group/group_list.html')

    def post(self):
        json = SysGroup.get_all_json()
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupListUserJoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        json = SysGroup.get_json_by_joined_user(uid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupListUserUnjoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        json = SysGroup.get_json_by_unjoined_user(uid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupListActionJoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        aid = self.get_argument('aid')
        json = SysGroup.get_json_by_joined_action(aid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupListActionUnjoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        aid = self.get_argument('aid')
        json = SysGroup.get_json_by_unjoined_action(aid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupAddHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = SysGroup.add(name, des, self.get_current_user().CODE)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class GroupDeleteHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        gids = str(self.get_argument('gid')).split(',')
        success_count = 0
        for gid in gids:
            err_code = SysGroup.delete(gid)
            if err_code == 0:
                success_count += 1
        if success_count > 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class GroupEditHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = SysGroup.update(gid, name, des)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class GroupUserAddHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        uid = str(self.get_argument('uid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupUser.add(gid, uid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class GroupUserDeleteHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        uid = str(self.get_argument('uid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupUser.delete(gid, uid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class GroupActionAddHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        aid = str(self.get_argument('aid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupAction.add(gid, aid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class GroupActionDeleteHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        aid = str(self.get_argument('aid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupAction.delete(gid, aid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)