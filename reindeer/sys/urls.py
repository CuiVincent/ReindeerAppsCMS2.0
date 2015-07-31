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
    (r'/content/(.*)', index.ContentHandler),
    (app_settings['login_url'], login.LoginHandler),
    (r'/logout', login.LogoutHandler),
    (r'/user_list', user.UserListHandler),
    (r'/user_add', user.UserAddHandler),
    (r'/user_edit', user.UserEditHandler),
    (r'/user_delete', user.UserDeleteHandler),
    (r'/group_list', group.GroupListHandler),
    (r'/group_joined_list', group.GroupJoinedListHandler),
    (r'/group_unjoined_list', group.GroupUnjoinedListHandler),
    (r'/group_add', group.GroupAddHandler),
    (r'/group_delete', group.GroupDeleteHandler),
    (r'/group_edit', group.GroupEditHandler),
    (r'/groups_user_add', group.GroupsUserAddHandler),
    (r'/groups_user_delete', group.GroupsUserDeleteHandler),
    (r'/action_list', action.ActionListHandler)

]

sys_modules = {'NavbarMenu': navbar_menu.NavbarMenuModule}