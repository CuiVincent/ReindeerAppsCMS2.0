__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import tornado.web
from tornado.escape import json_encode
from reindeer.sys.exceptions import BusinessRuleException
from reindeer.sys.model.sys_user import SysUser
import functools


class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        _ = self.get_local_translate_string
        err_page = 'sys/error.html'
        err_code = status_code
        msg = _('System error')
        info = self._reason
        if status_code == 404:
            msg = _('The link [%(uri)s] does not exist') % {'uri': self.request.uri}
            info = _('Make sure the link or contact the administrator')
        elif status_code == 500:
            if len(kwargs['exc_info']) > 1 and kwargs['exc_info'][1]:
                exception = kwargs['exc_info'][1]
                if isinstance(exception, BusinessRuleException):
                    err_code = exception.err_code
                    msg = exception.msg
                    info = exception.info
                else:
                    info = '[' + str(err_code) + ' - ' + info + ']' + str(exception)
        else:
            if err_code:
                info = '[' + str(err_code) + ']' + info
        if self.request.headers.get("__IS_AJAX_REQUEST") == 'true':
            self.write(json_encode({'success': False, 'err_code': err_code, 'msg': msg, 'info': info}))
        else:
            self.clear()  # 防止浏览器收到错误码后重定向
            if err_code >= 1000:
                err_title = 'ERROR'
            else:
                err_title = str(err_code)
            if err_code == 1000:
                func = 'toPage("' + self.application.settings["login_url"] + '");'
                func_text = _('Sign in')
            else:
                func = 'doBack();'
                func_text = _('Back')
            self.render(err_page, err_title=err_title, msg=msg, info=info, func=func, func_text=func_text)

    def get_current_user(self):
        user_id = self.get_current_user_id()
        return SysUser.get_by_id(user_id)

    def get_current_user_id(self):
        return self.get_secure_cookie('user_id') and str(self.get_secure_cookie('user_id'), 'utf-8') or None

    def get_page_arguments(self):
        r_start = int(self.get_argument('iDisplayStart'))
        r_length = int(self.get_argument('iDisplayLength'))
        r_search = self.get_argument('sSearch')
        r_sort_col = self.get_arguments('iSortCol_0')[0]
        r_sort_dir = self.get_arguments('sSortDir_0')[0]
        return [r_search, r_start, r_start + r_length, r_sort_col, r_sort_dir]

    def get_page_result_json(self, page):
        r_echo = self.get_argument('sEcho')
        json = page["data"]
        total = page["total"]
        search_total = page["search_total"]
        return '{"success": true, "aaData":' + json + ',"iTotalRecords":' + str(
            total) + ',"iTotalDisplayRecords":' + str(search_total) + ',"sEcho":' + str(r_echo) + '}'

    def get_local_translate_string(self, string):
        return self.get_browser_locale().translate(string)


class ErrorHandler(BaseHandler):
    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise BusinessRuleException(1000).translate(self.get_browser_locale())
        return method(self, *args, **kwargs)

    return wrapper