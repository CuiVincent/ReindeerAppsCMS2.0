__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String, Integer
from reindeer.sys.base_db_model import InfoTableModel
from reindeer.sys.exceptions import BusinessRuleException
from reindeer.sys.model.sys_group_action import SysGroupAction
from reindeer.sys import constants
from reindeer.sys.model.sys_group_user import SysGroupUser
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


    @classmethod
    def add(cls, name=None, type=None, url=None, des=None, parent=None, log=None, sort=None, icon_type=None, icon=None):
        action = SysAction(NAME=name, TYPE=type, URL=url, DES=des, PARENT=parent, LOG=log, SORT=sort,
                           ICON_TYPE=icon_type,
                           ICON=icon)
        if not str(action.PARENT).startswith(constants.action_root_prefix):
            if not cls.get_by_id(action.PARENT):
                raise BusinessRuleException(1101)
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
    def get_action_tree_by_user_and_parent(cls, user_id, parent, type):
        sql = " select t.*  from " + SysAction.__tablename__ + "  t , (select distinct ga.ACTION id from " + SysGroupAction.__tablename__ + " ga, " + SysGroupUser.__tablename__ + " gu where gu.USER ='" + user_id + "' and gu.GROUP = ga.GROUP) b  where b.id=t.ID and t.PARENT='" + parent + "'and t.TYPE = '" + type + "' order by t.sort asc"
        rows = cls.db_engine.execute(sql).fetchall()
        # ID | C_USER | C_DATE | NAME | TYPE | URL | DES | PARENT | LOG | SORT | ICON_TYPE | ICON
        actions = []
        for r in rows:
            actions.append(
                {'id': r[0], 'v_id': str(uuid.uuid1()), 'name': r[3], 'url': r[5], 'icon_type': r[10], 'icon': r[11],
                 'children': SysAction.get_action_tree_by_user_and_parent(user_id, r[0], type)})
        return actions

