__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from tornado.escape import json_encode
import reindeer.base.base_handler
from reindeer.sys.model.sys_group import SysGroup
from reindeer.sys.exceptions import BusinessRuleException
from reindeer.sys.model.sys_group_action import SysGroupAction
from reindeer.sys.model.sys_group_user import SysGroupUser


class GroupListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        self.render('sys/page/group/group_list.html')

    def post(self):
        page = SysGroup.get_page_json(*self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class GroupListUserJoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        page = SysGroup.get_page_json_by_joined_user(uid, *self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class GroupListUserUnjoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        page = SysGroup.get_page_json_by_unjoined_user(uid, *self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class GroupListActionJoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        aid = self.get_argument('aid')
        page = SysGroup.get_page_json_by_joined_action(aid, *self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class GroupListActionUnjoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        aid = self.get_argument('aid')
        page = SysGroup.get_page_json_by_unjoined_action(aid, *self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class GroupAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = SysGroup.add(name, des, self.get_current_user().CODE)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupDeleteHandler(reindeer.base.base_handler.BaseHandler):
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
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupEditHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = SysGroup.update(gid, name, des)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupUserAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = str(self.get_argument('uid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupUser.add(gid, uid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupUserDeleteHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = str(self.get_argument('uid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupUser.delete(gid, uid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupActionAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        aid = str(self.get_argument('aid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        clean = str(self.get_argument('clean'))
        if clean == 'by_group':
            err_code = SysGroupAction.delete_by_group_and_add(gid, aid)
        else:
            err_code = SysGroupAction.add(gid, aid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupActionDeleteHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        aid = str(self.get_argument('aid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = SysGroupAction.delete(gid, aid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code).translate(self.get_browser_locale())