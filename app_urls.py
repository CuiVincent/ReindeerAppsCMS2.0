__author__ = 'CuiVincent'
# encoding:utf-8
__all__ = ['app_urls', 'app_modules']

from reindeer.sys.urls import sys_urls, sys_modules
from reindeer.cms.urls import cms_urls, cms_modules

app_urls = []
app_urls.extend(sys_urls)
app_urls.extend(cms_urls)

app_modules = {}
app_modules.update(sys_modules)
app_modules.update(cms_modules)