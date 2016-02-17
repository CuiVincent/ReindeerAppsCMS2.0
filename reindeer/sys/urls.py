__author__ = 'CuiVincent'
__all__ = ['sys_urls', 'sys_modules']

from reindeer.sys.handler import index
from reindeer.sys.handler import login
from reindeer.sys.handler import user
from reindeer.sys.handler import group
from reindeer.sys.handler import action
from reindeer.sys.module import navbar_menu
from app_settings import app_settings

sys_urls = [
    (r'/', index.IndexHandler),
    (app_settings['login_url'], login.LoginHandler),
    (r'/logout', login.LogoutHandler),
    (r'/user', user.UserListHandler),
    (r'/user_group_joined', user.UserListGroupJoinedHandler),
    (r'/user_group_unjoined', user.UserListGroupUnjoinedHandler),
    (r'/user_add', user.UserAddHandler),
    (r'/user_edit', user.UserEditHandler),
    (r'/user_delete', user.UserDeleteHandler),
    (r'/group', group.GroupListHandler),
    (r'/group_user_joined', group.GroupListUserJoinedHandler),
    (r'/group_user_unjoined', group.GroupListUserUnjoinedHandler),
    (r'/group_action_joined', group.GroupListActionJoinedHandler),
    (r'/group_action_unjoined', group.GroupListActionUnjoinedHandler),
    (r'/group_add', group.GroupAddHandler),
    (r'/group_delete', group.GroupDeleteHandler),
    (r'/group_edit', group.GroupEditHandler),
    (r'/group_user_add', group.GroupUserAddHandler),
    (r'/group_user_delete', group.GroupUserDeleteHandler),
    (r'/group_action_add', group.GroupActionAddHandler),
    (r'/group_action_delete', group.GroupActionDeleteHandler),
    (r'/action', action.ActionListHandler),
    (r'/action_group_joined', action.ActionListGroupJoinedHandler),
    (r'/action_add', action.ActionAddHandler),
    (r'/action_edit', action.ActionEditHandler),
    (r'/action_delete', action.ActionDeleteHandler)
]

sys_modules = {'NavbarMenu': navbar_menu.NavbarMenuModule, 'NavbarScaleMenu': navbar_menu.NavbarScaleMenuModule}