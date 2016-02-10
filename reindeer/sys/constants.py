__author__ = 'cui'
# -*- coding: utf8 -*-

action_root_prefix = '[ACTION_ROOT]'
action_root_name = 'root node'
action_root_main_parent = action_root_prefix + 'MAIN_MENU'
action_root_title_parent = action_root_prefix + 'TITLE_MENU'

# 操作权限类型-菜单
action_type_menu_menu = '0'
#操作权限类型-可扩展菜单
action_type_scalable_menu_menu = '1'

#用户状态-正常
user_status_normal = '1'
#用户状态-禁用
user_status_forbidden = '2'

str_user_unknown = '[UNKNOWN]'
str_user_sys = '[SYS]'

err_codes = {
    0: ['Successed', 'Operation successed'],
    1: ['Failed', 'Operation failed'],
    2: ['Unknown Error', 'Try later'],
    1000: ['Not signed', 'You are not signed or sign has expired'],
    1001: ['Sign in failed', 'Incorrect username'],
    1002: ['Sign in failed', 'Incorrect password'],
    1003: ['Sign in failed', 'Account is desabled'],
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