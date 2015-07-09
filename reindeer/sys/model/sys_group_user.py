__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from reindeer.sys.base_db_model import NormalTableModel


class SysGroupUser(NormalTableModel):
    __tablename__ = 'RA_SYS_GROUP_USER'
    GROUP = Column(String(50), primary_key=True)
    USER = Column(String(50), primary_key=True)

    @classmethod
    def add(cls, group, user):
        user = not isinstance(user, list) and [user] or user
        for u in user:
            group_user = SysGroupUser(USER=u, GROUP=group)
            if not group_user.get():
                cls.db_session.add(group_user)
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    def get(self):
        item = self.db_session.query(SysGroupUser).filter(
            SysGroupUser.GROUP == self.GROUP, SysGroupUser.USER == self.USER).first()
        return item

    @classmethod
    def get_by_group_and_user(cls, group, user):
        item = cls.db_session.query(SysGroupUser).filter(
            SysGroupUser.GROUP == group, SysGroupUser.USER == user).first()
        return item