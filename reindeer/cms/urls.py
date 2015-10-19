__author__ = 'CuiVincent'
__all__ = ['cms_urls', 'cms_modules']

from reindeer.cms.handler import app
from reindeer.cms.handler import user

cms_urls = [
    (r'/cms/app_list', app.AppListHandler),
    (r'/cms/user_list', user.UserListHandler),
    (r'/cms/user_list_group_joined', user.UserListGroupJoinedHandler),
    (r'/cms/user_list_group_unjoined', user.UserListGroupUnjoinedHandler),
    (r'/cms/user_add', user.UserAddHandler),
    (r'/cms/user_edit', user.UserEditHandler),
    (r'/cms/user_delete', user.UserDeleteHandler)
]

cms_modules = {}