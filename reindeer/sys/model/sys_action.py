__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String, Integer
from reindeer.sys.base_db_model import InfoTableModel
from reindeer.sys.model.sys_group_action import SysGroupAction
from reindeer.sys.model.sys_group_user import SysGroupUser
from reindeer.sys.model.sys_group import SysGroup
from reindeer.sys import constants
from sqlalchemy.orm import relationship
import uuid


class SysAction(InfoTableModel):
    __tablename__ = 'RA_SYS_ACTION'
    NAME = Column(String(100))
    TYPE = Column(String(2), default=constants.action_type_menu_menu)
    URL = Column(String(200))
    DES = Column(String(1000))
    PARENT = Column(String(50), default=constants.action_root_main_parent)
    LOG = Column(String(1), default='1')
    SORT = Column(Integer)
    ICON_TYPE = Column(String(1), default='1')
    ICON = Column(String(200))
    groups = relationship('SysGroup', secondary='RA_SYS_GROUP_ACTION')

    @classmethod
    def add(cls, name=None, type=None, url=None, des=None, parent=None, log=None, sort=None, icon_type=None, icon=None):
        action = SysAction(NAME=name, TYPE=type, URL=url, DES=des, PARENT=parent, LOG=log, SORT=sort,
                           ICON_TYPE=icon_type,
                           ICON=icon)
        if not str(action.PARENT).startswith(constants.action_root_prefix):
            if not cls.get_by_id(action.PARENT):
                return 1151
        cls.db_session.add(action)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (action.ID):
            return 0
        else:
            return 1

    @classmethod
    def add_and_get(cls, name=None, type=None, url=None, des=None, parent=None, log=None, sort=None, icon_type=None,
                    icon=None):
        action = SysAction(NAME=name, TYPE=type, URL=url, DES=des, PARENT=parent, LOG=log, SORT=sort,
                           ICON_TYPE=icon_type,
                           ICON=icon)
        if not str(action.PARENT).startswith(constants.action_root_prefix):
            if not cls.get_by_id(action.PARENT):
                return None
        cls.db_session.add(action)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (action.ID):
            return action
        else:
            return None

    @classmethod
    def get_by_id(cls, id):
        item = cls.db_session.query(SysAction).filter(SysAction.ID == id).first()
        return item

    @classmethod
    def get_tree_by_user_and_parent(cls, user_id, parent, type):
        items = cls.db_session.query(SysAction).join(SysGroupAction).join(SysGroup).join(SysGroupUser).filter(
            SysGroupUser.USER == user_id, SysAction.PARENT == parent, SysAction.TYPE == type).all()
        actions = []
        for item in items:
            actions.append(
                {'id': item.ID, 'v_id': str(uuid.uuid1()), 'name': item.NAME, 'url': item.URL,
                 'icon_type': item.ICON_TYPE, 'icon': item.ICON,
                 'children': SysAction.get_tree_by_user_and_parent(user_id, item.ID, type)})
        return actions

    @classmethod
    def get_tree_by_parent(cls, parent, type):
        items = cls.db_session.query(SysAction).filter(SysAction.PARENT == parent, SysAction.TYPE == type).all()
        actions = []
        for item in items:
            actions.append(
                {'id': item.ID, 'v_id': str(uuid.uuid1()), 'name': item.NAME, 'url': item.URL,
                 'icon_type': item.ICON_TYPE, 'icon': item.ICON,
                 'children': SysAction.get_tree_by_parent(item.ID, type)})
        return actions