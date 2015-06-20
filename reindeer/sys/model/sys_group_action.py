__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from reindeer.sys.base_db_model import NormalTableModel


class SysGroupAction(NormalTableModel):
    __tablename__ = 'RA_SYS_GROUP_ACTION'
    GROUP = Column(String(50), primary_key=True)
    ACTION = Column(String(50), primary_key=True)

    @classmethod
    def add(cls, group, action):
        action = not isinstance(action, list) and [action] or action
        for a in action:
            group_action = SysGroupAction(ACTION=a, GROUP=group)
            if not group_action.get():
                cls.db_session.add(group_action)
        try:
            cls.db_session.commit()
            return True
        except:
            cls.db_session.rollback()
            return False

    def get(self):
        item = self.db_session.query(SysGroupAction).filter(
            SysGroupAction.GROUP == self.GROUP, SysGroupAction.ACTION == self.ACTION).first()
        return item

    @classmethod
    def get_by_group_and_action(cls, group, action):
        item = cls.db_session.query(SysGroupAction).filter(
            SysGroupAction.GROUP == group, SysGroupAction.ACTION == action).first()
        return item