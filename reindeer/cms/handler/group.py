__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from tornado.escape import json_encode
import reindeer.base.base_handler
from reindeer.cms.model.cms_group import CmsGroup
from reindeer.cms.exceptions import CmsBusinessRuleException
from reindeer.cms.model.cms_group_user import CmsGroupUser


class GroupListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        self.render('cms/page/group/group_list.html')

    def post(self):
        json = CmsGroup.get_all_json()
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupListUserJoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        json = CmsGroup.get_json_by_joined_user(uid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupListUserUnjoinedHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = self.get_argument('uid')
        json = CmsGroup.get_json_by_unjoined_user(uid)
        r_json = '{"success": true, "aaData":' + json + '}'
        print(r_json)
        return self.write(r_json)


class GroupAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = CmsGroup.add(name, des, self.get_current_user().CODE)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupDeleteHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        gids = str(self.get_argument('gid')).split(',')
        success_count = 0
        for gid in gids:
            err_code = CmsGroup.delete(gid)
            if err_code == 0:
                success_count += 1
        if success_count > 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupEditHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        gid = self.get_argument('gid')
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = CmsGroup.update(gid, name, des)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupUserAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = str(self.get_argument('uid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = CmsGroupUser.add(gid, uid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class GroupUserDeleteHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        uid = str(self.get_argument('uid')).split(',')
        gid = str(self.get_argument('gid')).split(',')
        err_code = CmsGroupUser.delete(gid, uid)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())
