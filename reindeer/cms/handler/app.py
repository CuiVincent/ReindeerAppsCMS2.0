__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import reindeer.base.base_handler
from reindeer.cms.model.cms_app import CmsApp


class AppListHandler(reindeer.base.base_handler.BaseHandler):
    def get(self):
        self.render('cms/page/app/app_list.html')

    def post(self):
        json = CmsApp.get_all_json()
        r_json = '{"success": true, "data":' + json + '}'
        print(r_json)
        return self.write(r_json)