__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

err_codes = {
    0: ['成功', '操作成功'],
    1: ['失败', '操作失败'],
    11000: ['未登录', '您暂未登录或登录已过期'],
    11001: ['登录失败', '您所输入的账号不存在'],
    11002: ['登录失败', '密码错误'],
    11003: ['登录失败', '该账号已被停止使用'],
    11051: ['新建失败', '该用户名已存在'],
    11052: ['删除失败', '该用户不存在'],
    11053: ['编辑失败', '该用户不存在'],
    11101: ['删除失败', '该组织不存在'],
    11102: ['编辑失败', '该组织不存在'],
    11151: ['创建失败', '父节点不存在'],
    11152: ['删除失败', '该操作权限不存在'],
    11153: ['删除失败', '该节点不是叶子节点'],
    11154: ['编辑失败', '该操作权限不存在']
}


class CmsBusinessRuleException(Exception):
    def __init__(self, err_code):
        self.err_code = err_code
        try:
            self.msg = err_codes[self.err_code][0]
        except KeyError:
            self.msg = '未知错误'
        try:
            self.info = err_codes[self.err_code][1]
        except KeyError:
            self.info = '请稍后再试'

    def __str__(self):
        message = "BusinessRule [%d - %s] %s" % (self.err_code, self.msg, self.info)
        return message
