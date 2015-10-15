__author__ = 'CuiVincent'
__all__ = ['cms_urls', 'cms_modules']

from reindeer.cms.handler import app

cms_urls = [
    (r'/cms/app_list', app.AppListHandler),
]

cms_modules = {}