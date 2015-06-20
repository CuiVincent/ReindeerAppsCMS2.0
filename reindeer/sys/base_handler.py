__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import tornado.web
from tornado.escape import json_encode
from reindeer.sys.exceptions import BusinessRuleException
from reindeer.sys.model.sys_user import SysUser
import functools


class BaseHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        err_page = 'sys/error.html'
        err_code = status_code
        msg = '系统错误'
        info = self._reason
        if status_code == 404:
            msg = '您所访问的链接[' + self.request.uri + ']不存在'
            info = '请确认链接地址或联系管理员'
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
                func = 'toPage("'+self.application.settings["login_url"]+'");'
                func_text = '登录'
            else:
                func = 'back();'
                func_text = '返回'
            self.render(err_page, err_title=err_title, msg=msg, info=info, func=func, func_text=func_text)

    def get_current_user(self):
        user_id = self.get_secure_cookie('user_id')
        return SysUser.get_by_id(user_id)


class ErrorHandler(BaseHandler):
    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

    def check_xsrf_cookie(self):
        pass


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise BusinessRuleException(1000)
        return method(self, *args, **kwargs)
    return wrapper