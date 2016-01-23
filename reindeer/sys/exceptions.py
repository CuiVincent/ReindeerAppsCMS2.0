__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

err_codes = {
    0: ['成功', '操作成功'],
    1: ['失败', '操作失败'],
    1000: ['未登录', '您暂未登录或登录已过期'],
    1001: ['登录失败', '您所输入的账号不存在'],
    1002: ['登录失败', '密码错误'],
    1003: ['登录失败', '该账号已被停止使用'],
    1051: ['新建失败', '该用户名已存在'],
    1052: ['删除失败', '该用户不存在'],
    1053: ['编辑失败', '该用户不存在'],
    1101: ['删除失败', '该组织不存在'],
    1102: ['编辑失败', '该组织不存在'],
    1151: ['创建失败', '父节点不存在'],
    1152: ['删除失败', '该操作权限不存在'],
    1153: ['删除失败', '该节点不是叶子节点'],
    1154: ['编辑失败', '该操作权限不存在']
}


class BusinessRuleException(Exception):
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
