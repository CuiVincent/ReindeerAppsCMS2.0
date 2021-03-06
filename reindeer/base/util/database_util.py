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
from reindeer.sys import constants as sys_constants
from reindeer.cms.model.cms_app import CmsApp
from reindeer.cms.model.cms_action import CmsAction
from reindeer.cms.model.cms_group import CmsGroup
from reindeer.cms.model.cms_group_action import CmsGroupAction
from reindeer.cms.model.cms_group_user import CmsGroupUser
from reindeer.cms.model.cms_user import CmsUser
from reindeer.cms.model.cms_action_relation import CmsActionRelation
from reindeer.cms.model.cms_layout import CmsLayout


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
        user_id = SysUser.add_and_get('reindeer', '超级管理员', '111', 1, sys_constants.str_user_sys).ID
        group_id = SysGroup.add_and_get('admin', '系统管理组').ID
        SysGroupUser.add(group_id, user_id)
        sys_action_id = SysAction.add_and_get(name='系统管理', url='/sys_manager',
                                              parent=sys_constants.action_root_main_parent,
                                              sort=1, icon='glyphicon-cog').ID
        sys_action_group_id = SysAction.add_and_get(name='组织管理', url='/group', parent=sys_action_id, sort=1,
                                                    icon='glyphicon-flag').ID
        sys_action_user_id = SysAction.add_and_get(name='用户管理', url='/user', parent=sys_action_id, sort=2,
                                                   icon='glyphicon-user').ID
        sys_action_action_id = SysAction.add_and_get(name='操作权限管理', url='/action', parent=sys_action_id, sort=3,
                                                     icon='glyphicon-eye-close').ID
        cms_action_id = SysAction.add_and_get(name='AppCMS', url='/app_manager',
                                              parent=sys_constants.action_root_main_parent,
                                              sort=2, icon='glyphicon-phone').ID
        cms_action_app_id = SysAction.add_and_get(name='App管理', url='/cms/app',
                                                  type=sys_constants.action_type_scalable_menu_menu,
                                                  scale_script='__import__(\'reindeer\').cms.model.cms_app.CmsApp.get_tree_by_c_user(\'/cms/app\',self.get_current_user_id())',
                                                  parent=cms_action_id, sort=1,
                                                  icon='glyphicon-th-large').ID
        cms_action_group_id = SysAction.add_and_get(name='组织管理', url='/cms/group', parent=cms_action_id, sort=2,
                                                    icon='glyphicon-flag').ID
        cms_action_user_id = SysAction.add_and_get(name='用户管理', url='/cms/user', parent=cms_action_id, sort=3,
                                                   icon='glyphicon-user').ID
        cms_action_layout_id = SysAction.add_and_get(name='布局管理', url='/cms/layout', parent=cms_action_id, sort=4,
                                                     icon='glyphicon-blackboard').ID
        cms_action_data_id = SysAction.add_and_get(name='数据管理', url='/cms/data', parent=cms_action_id, sort=5,
                                                   icon='glyphicon-hdd').ID
        cms_action_platform_id = SysAction.add_and_get(name='平台管理', url='/cms/platform', parent=cms_action_id,
                                                       sort=6,
                                                       icon='glyphicon-phone').ID

        SysGroupAction.add(group_id, [sys_action_id, sys_action_group_id, sys_action_user_id, sys_action_action_id])
        SysGroupAction.add(group_id, [cms_action_id, cms_action_app_id, cms_action_group_id,
                                      cms_action_user_id, cms_action_layout_id, cms_action_data_id,
                                      cms_action_platform_id])

        DatabaseUtil.init_test_data()

        CmsApp.add(name="TEST_APP", code="test.com", c_user=user_id)
        CmsUser
        CmsAction
        CmsGroup
        CmsGroupUser
        CmsGroupAction
        CmsActionRelation
        CmsLayout

    @staticmethod
    def init(db_instance):
        DatabaseUtil.drop_all_table(db_instance)
        DatabaseUtil.create_all_table(db_instance)
        DatabaseUtil.init_database_data()

    # 以下制造测试数据
    @staticmethod
    def init_test_data():
        for x in ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"]:
            for i in range(100, 200):
                SysUser.add_and_get('TEST-CODE-' + x + str(i), 'TEST-NAME-' + x + str(i), '111', 1).ID