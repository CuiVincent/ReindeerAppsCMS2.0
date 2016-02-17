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
    0: ['Succeeded', 'Operation succeeded'],
    1: ['Failed', 'Operation failed'],
    2: ['Unknown Error', 'Try later'],
    1000: ['Not signed', 'You are not signed or sign has expired'],
    1001: ['Sign in failed', 'Incorrect username'],
    1002: ['Sign in failed', 'Incorrect password'],
    1003: ['Sign in failed', 'Account is disabled'],
    1051: ['Create failed', 'This username already exists'],
    1052: ['Delete failed', 'This user does not exist'],
    1053: ['Edit failed', 'This user does not exist'],
    1101: ['Delete failed,' 'The group does not exist'],
    1102: ['Edit failed,' 'The group does not exist'],
    1151: ['Create failed', 'Parent node does not exist'],
    1152: ['Delete failed,' 'The action does not exist'],
    1153: ['Delete failed,' 'The node is not a leaf node'],
    1154: ['Edit failed,' 'The action does not exist']
}