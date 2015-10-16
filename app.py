__author__ = 'CuiVincent'
# encoding:utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import reindeer
from tornado.options import define, options
from app_settings import app_settings, db_settings
from app_urls import app_urls, app_modules
from reindeer.base.util.database_util import DatabaseInstance, DatabaseUtil
from reindeer.base.base_db_model import InfoTableModel, NormalTableModel

define("port", default=9000, help="run on the given port", type=int)


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
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
