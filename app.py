__author__ = 'CuiVincent'
# encoding:utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import reindeer
from tornado.options import options
from app_settings import app_settings, app_listen_settings
from app_urls import app_urls, app_modules


class Application(tornado.web.Application):
    def __init__(self, handlers, **settings):
        settings['ui_modules'] = app_modules
        tornado.web.Application.__init__(self, handlers, **settings)
        tornado.web.ErrorHandler = reindeer.base.base_handler.ErrorHandler
        Application.instance = self

    @classmethod
    def instance(cls):
        return cls.instance


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(app_urls, **app_settings))
    print(app_listen_settings)
    if app_listen_settings['ip']:
        http_server.listen(app_listen_settings['port'], app_listen_settings['ip'])
    else:
        http_server.listen(app_listen_settings['port'])
    tornado.ioloop.IOLoop.instance().start()
