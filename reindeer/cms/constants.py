__author__ = 'cui'
# -*- coding: utf8 -*-

action_root = '[ACTION_ROOT]'
action_root_name = '根节点'

# 操作权限类型-独立页面
action_type_page = '0'

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
app_control_default = app_control_login + '|' + app_control_action + '|' + app_control_data

#图标类型-默认
icon_default = '0'
#图标类型-客户端指定
icon_client = '1'
#图标类型-上传
icon_upload = '2'

