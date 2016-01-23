__author__ = 'CuiVincent'
__all__ = ['cms_urls', 'cms_modules']

from reindeer.cms.handler import app
from reindeer.cms.handler import user
from reindeer.cms.handler import group

cms_urls = [
    (r'/cms/app_list', app.AppListHandler),
    (r'/cms/app_add', app.AppAddHandler),
    (r'/cms/app_delete', app.AppDeleteHandler),
    (r'/cms/user_list', user.UserListHandler),
    (r'/cms/user_list_group_joined', user.UserListGroupJoinedHandler),
    (r'/cms/user_list_group_unjoined', user.UserListGroupUnjoinedHandler),
    (r'/cms/user_add', user.UserAddHandler),
    (r'/cms/user_edit', user.UserEditHandler),
    (r'/cms/user_delete', user.UserDeleteHandler),
    (r'/cms/group_list', group.GroupListHandler),
    (r'/cms/group_list_user_joined', group.GroupListUserJoinedHandler),
    (r'/cms/group_list_user_unjoined', group.GroupListUserUnjoinedHandler),
    (r'/cms/group_add', group.GroupAddHandler),
    (r'/cms/group_delete', group.GroupDeleteHandler),
    (r'/cms/group_edit', group.GroupEditHandler),
    (r'/cms/group_user_add', group.GroupUserAddHandler),
    (r'/cms/group_user_delete', group.GroupUserDeleteHandler),
]

cms_modules = {}