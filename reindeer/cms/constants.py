from reindeer.sys.constants import err_codes

__author__ = 'cui'
# -*- coding: utf8 -*-

action_root = '[ACTION_ROOT]'
action_root_name = 'root node'

# 操作权限类型-独立页面
action_type_page = '0'
# 操作权限类型-复数页面
action_type_multiple_page = '1'

disable_log = '0'
enable_log = '1'

# 用户状态-正常
user_status_normal = '1'
# 用户状态-禁用
user_status_forbidden = '2'

app_type_default = '0'

#应用类型-使用服务器进行登陆
app_control_login = '1'
#应用类型-使用服务器权限管理
app_control_action = '2'
#应用类型-使用服务器获取数据
app_control_data = '3'

#图标类型-默认
icon_default = '0'
#图标类型-客户端指定
icon_client = '1'
#图标类型-上传
icon_upload = '2'


layout_root = '[LAYOUT_ROOT]'
#默认转场方式
layout_trans_default = '0'

cms_err_codes = {
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
    11154: ['编辑失败', '该操作权限不存在'],
    11201: ['删除失败', '该APP不存在']
}

cms_err_codes.update(err_codes)