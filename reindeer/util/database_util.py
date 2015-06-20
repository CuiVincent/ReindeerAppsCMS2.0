__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app_settings import db_settings
from reindeer.sys.model.sys_group import SysGroup
from reindeer.sys.model.sys_user import SysUser
from reindeer.sys.model.sys_action import SysAction
from reindeer.sys.model.sys_group_user import SysGroupUser
from reindeer.sys.model.sys_group_action import SysGroupAction
from reindeer.sys import constants


class DatabaseInstance:
    def __init__(self, settings=db_settings, base_db_model_class=[]):
        self.__db_engine = None
        self.__db_session = None
        self.__base_db_model_classes = []
        DatabaseUtil.create_db_session(self, settings)
        self.add_base_db_model_classes(base_db_model_class)

    def bind(self, engine, session):
        self.__db_engine = engine
        self.__db_session = session

    def add_base_db_model_classes(self, base_db_model_class):
        new_classes = not isinstance(base_db_model_class, list) and [
            base_db_model_class] or base_db_model_class
        for clazz in new_classes:
            if clazz not in self.__base_db_model_classes:
                clazz.db_session = self.__db_session
                clazz.db_engine = self.__db_engine
                self.__base_db_model_classes.append(clazz)

    @property
    def db_engine(self):
        return self.__db_engine

    @property
    def db_session(self):
        return self.__db_session

    @property
    def base_db_model_classes(self):
        return self.__base_db_model_classes

    def create_all_table(self):
        DatabaseUtil.create_all_table(self)

    def drop_all_table(self):
        DatabaseUtil.drop_all_table(self)


class DatabaseUtil:
    @staticmethod
    def get_db_url(settings):
        url = ''
        if settings['driven'].lower() == 'mysql':
            url = 'mysql://' + settings['user'] + ':' + settings['password'] + '@' + settings['host'] + '/' + \
                  settings['database']
        else:
            pass
        return url

    @staticmethod
    def create_db_session(db_instance, settings):
        db_engine = create_engine(DatabaseUtil.get_db_url(settings), pool_recycle=60,
                                  connect_args={"charset": "utf8"}, echo=True)
        db_session = scoped_session(sessionmaker(bind=db_engine))
        db_instance.bind(db_engine, db_session)

    @staticmethod
    def create_all_table(db_instance):
        for clazz in db_instance.base_db_model_classes:
            clazz.metadata.create_all(bind=db_instance.db_engine)

    @staticmethod
    def drop_all_table(db_instance):
        for clazz in db_instance.base_db_model_classes:
            clazz.metadata.drop_all(bind=db_instance.db_engine)

    @staticmethod
    def init_database_data():
        user_id = SysUser.add('reindeer', '超级管理员', '111', 1, constants.str_user_sys).ID
        group_id = SysGroup.add('admin', '系统管理组').ID
        SysGroupUser.add(group_id, user_id)
        sys_action_id = SysAction.add(name='系统管理', url='sys_manager', parent=constants.action_root_main_parent,
                                      sort=1, icon='icon-folder-close').ID
        sys_action_group_id = SysAction.add(name='用户组管理', url='group_list', parent=sys_action_id, sort=1,
                                            icon='icon-user').ID
        sys_action_user_id = SysAction.add(name='用户管理', url='user_list', parent=sys_action_id, sort=2,
                                           icon='icon-user').ID
        sys_action_action_id = SysAction.add(name='操作权限管理', url='action_list', parent=sys_action_id, sort=3,
                                             icon='icon-folder-close').ID
        app_action_id = SysAction.add(name='App管理', url='app_manager', parent=constants.action_root_main_parent,
                                      sort=2, icon='icon-folder-close').ID
        app_action_platform_id = SysAction.add(name='平台管理', url='12', parent=app_action_id, sort=1,
                                               icon='icon-folder-close').ID
        SysGroupAction.add(group_id, [sys_action_id, sys_action_group_id, sys_action_user_id, sys_action_action_id])
        SysGroupAction.add(group_id, [app_action_id, app_action_platform_id])

        DatabaseUtil.initTestData()

    @staticmethod
    def init(db_instance):
        # DatabaseUtil.drop_all_table(db_instance) #不知为什么会锁表
        DatabaseUtil.create_all_table(db_instance)
        DatabaseUtil.init_database_data()

    # 以下制造测试数据
    @staticmethod
    def initTestData():
        for x in ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]:
            for i in range(100, 200):
                SysUser.add('TEST-CODE-'+x+str(i),'TEST-NAME-'+x+str(i), '111', 1).ID