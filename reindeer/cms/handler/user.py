__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from tornado.escape import json_encode
import reindeer.base.base_handler
from reindeer.cms.model.cms_user import CmsUser
from reindeer.cms.exceptions import CmsBusinessRuleException


class UserListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        self.render('cms/page/user/user_list.html')

    def post(self):
        page = CmsUser.get_page_json(*self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class UserListGroupJoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        page = CmsUser.get_page_json_by_joined_groupid(gid, *self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class UserListGroupUnjoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        page = CmsUser.get_page_json_by_unjoined_groupid(gid, *self.get_page_arguments())
        r_json = self.get_page_result_json(page)
        print(r_json)
        return self.write(r_json)


class UserAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        code = self.get_argument('code')
        name = self.get_argument('name')
        status = self.get_argument('status') if self.get_argument('status') else 1
        err_code = CmsUser.add(code, name, "111", status, self.get_current_user().CODE)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class UserDeleteHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uids = str(self.get_argument('uid')).split(',')
        success_count = 0
        for uid in uids:
            err_code = CmsUser.delete(uid)
            if err_code == 0:
                success_count += 1
        if success_count > 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class UserEditHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        status = self.get_argument('status') if self.get_argument('status') else 1
        name = self.get_argument('name')
        err_code = CmsUser.update(uid, name, status)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


