__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.base.base_handler
from reindeer.cms.model.cms_app import CmsApp
from tornado.escape import json_encode
from reindeer.cms.exceptions import CmsBusinessRuleException


class AppListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        self.render('cms/page/app/app_list.html')

    def post(self):
        json = CmsApp.get_all_json()
        r_json = '{"success": true, "data":' + json + '}'
        print(r_json)
        return self.write(r_json)


class AppAddHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        name = self.get_argument('name')
        des = self.get_argument('des')
        err_code = CmsApp.add(name=name, des=des, c_user=self.get_current_user().CODE)
        if err_code == 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())


class AppDeleteHandler(reindeer.base.base_handler.BaseHandler):
    def post(self):
        aids = str(self.get_argument('aid')).split(',')
        success_count = 0
        for aid in aids:
            err_code = CmsApp.delete(aid)
            if err_code == 0:
                success_count += 1
        if success_count > 0:
            return self.write(json_encode({'success': True}))
        else:
            raise CmsBusinessRuleException(err_code).translate(self.get_browser_locale())
