__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from tornado.escape import json_encode
import reindeer.base.base_handler
from reindeer.cms import constants
from reindeer.cms.model.cms_app import CmsApp
from reindeer.cms.model.cms_action import CmsAction
from reindeer.cms.exceptions import CmsBusinessRuleException


class ActionListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self, aid):
        app = CmsApp.get_by_id(aid)
        if app.C_USER == self.get_current_user_id():
            self.render('cms/page/action/action_list.html', app_id=aid, app_name=app.NAME)
        else:
            raise CmsBusinessRuleException(11155).translate(self.get_browser_locale())

    def post(self, aid):
        actions = CmsAction.get_ratree_by_parent_and_app(constants.action_root, aid)
        return self.write(json_encode({'success': True, 'data': actions}))


# class ActionListGroupJoinedHandler(reindeer.base.base_handler.BaseHandler):
# def post(self):
# gid = self.get_argument('gid')
# actions = SysAction.get_ratree_checked_by_group(gid)
# return self.write(json_encode({'success': True, 'data': actions}))


class ActionAddHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        id = self.get_argument('id')
        action = CmsAction.get_json_by_id(id)
        if action:
            return self.write(json_encode({'success': True, 'data': action}))
        else:
            raise CmsBusinessRuleException(11151).translate(self.get_browser_locale())

    def post(self):
        app = self.get_argument('aid')
        name = self.get_argument('name')
        type = self.get_argument('type')
        des = self.get_argument('des')
        parent = self.get_argument('pid')
        if not parent:
            if CmsAction.get_by_parent_and_app(constants.action_root, app):
                raise CmsBusinessRuleException(11156).translate(self.get_browser_locale())
            else:
                parent = constants.action_root
        sort = self.get_argument('sort')

        err_code = CmsAction.add(name=name, type=type, des=des, parent=parent, sort=sort, app=app)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


            # class ActionDeleteHandler(reindeer.base.base_handler.BaseHandler):
            # def post(self):
            # aids = str(self.get_argument('aid')).split(',')
            # success_count = 0
            # for aid in aids:
            # err_code = SysAction.delete(aid)
            # if err_code == 0:
            # success_count += 1
            # if success_count > 0:
            #             return self.write(json_encode({'success': True}))
            #         else:
            #             raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())
            #
            #
            # class ActionEditHandler(reindeer.base.base_handler.BaseHandler):
            #     def get(self):
            #         id = self.get_argument('id')
            #         action = SysAction.get_json_by_id(id)
            #         if action:
            #             parent_action = SysAction.get_parent_by_id(id)
            #             return self.write(json_encode({'success': True, 'data': action,
            #                                            'parent_data': parent_action and parent_action.NAME or constants.action_root_name}))
            #         else:
            #             raise CmsBusinessRuleException(1152).translate(self.get_browser_locale())
            #
            #     def post(self):
            #         id = self.get_argument('aid')
            #         name = self.get_argument('name')
            #         des = self.get_argument('des')
            #         url = self.get_argument('url')
            #         sort = self.get_argument('sort')
            #         icon = self.get_argument('icon')
            #         type = self.get_argument('type')
            #         scale_script = self.get_argument('scale_script')
            #         err_code = SysAction.update(id=id, name=name, url=url, type=type, scale_script=scale_script, des=des,
            #                                     sort=sort, icon=icon)
            #         if err_code == 0:
            #             return self.write(json_encode({'success': True}))
            #         else:
            #             raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())