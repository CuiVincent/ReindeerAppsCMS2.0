__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.sys.base_handler
from reindeer.sys.model.sys_user import SysUser
from tornado.escape import json_encode

from reindeer.sys.exceptions import BusinessRuleException


class UserListHandler(reindeer.sys.base_handler.BaseHandler):
    def get(self):
        self.render('sys/page/user/user_list.html')

    def post(self):
        r_echo = self.get_argument('sEcho')
        r_start = int(self.get_argument('iDisplayStart'))
        r_length = int(self.get_argument('iDisplayLength'))
        r_search = self.get_argument('sSearch')
        r_sort_col = self.get_arguments('iSortCol_0')[0]
        r_sort_dir = self.get_arguments('sSortDir_0')[0]

        json = SysUser.get_slice_json(r_search, r_start, r_start + r_length, r_sort_col, r_sort_dir)
        total = SysUser.get_all_count()
        slice_total = SysUser.get_slice_count(r_search)
        r_json = '{"success": true, "aaData":' + json + ',"iTotalRecords":' + str(
            total) + ',"iTotalDisplayRecords":' + str(slice_total) + ',"sEcho":' + str(r_echo) + '}'
        print(r_json)
        return self.write(r_json)


class UserListGroupJoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        json = SysUser.get_slice_json_by_joined_groupid(gid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class UserListGroupUnjoinedHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        json = SysUser.get_slice_json_by_unjoined_groupid(gid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class UserAddHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        code = self.get_argument('code')
        name = self.get_argument('name')
        status = self.get_argument('status') if self.get_argument('status') else 1
        err_code = SysUser.add(code, name, "111", status, self.get_current_user().CODE)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class UserDeleteHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        uids = str(self.get_argument('uid')).split(',')
        success_count = 0
        for uid in uids:
            err_code = SysUser.delete(uid)
            if err_code == 0:
                success_count += 1
        if success_count > 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


class UserEditHandler(reindeer.sys.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        status = self.get_argument('status') if self.get_argument('status') else 1
        name = self.get_argument('name')
        err_code = SysUser.update(uid, name, status)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise BusinessRuleException(err_code)


