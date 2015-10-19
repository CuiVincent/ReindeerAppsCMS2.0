__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String, ForeignKey
from reindeer.base.base_db_model import InfoTableModel


class CmsGroupUser(InfoTableModel):
    __tablename__ = 'RA_CMS_GROUP_USER'
    GROUP = Column(String(50), ForeignKey('RA_CMS_GROUP.ID', ondelete='CASCADE', onupdate='CASCADE'))
    USER = Column(String(50), ForeignKey('RA_CMS_USER.ID', ondelete='CASCADE', onupdate='CASCADE'))

    @classmethod
    def add(cls, group, user):
        user = not isinstance(user, list) and [user] or user
        group = not isinstance(group, list) and [group] or group
        for u in user:
            for g in group:
                group_user = CmsGroupUser(USER=u, GROUP=g)
                if not group_user.get():
                    cls.db_session.add(group_user)
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def delete(cls, group, user):
        user = not isinstance(user, list) and [user] or user
        group = not isinstance(group, list) and [group] or group
        for u in user:
            for g in group:
                items = cls.db_session.query(CmsGroupUser).filter(CmsGroupUser.GROUP == g, CmsGroupUser.USER == u)
                if items:
                    items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    def get(self):
        item = self.db_session.query(CmsGroupUser).filter(
            CmsGroupUser.GROUP == self.GROUP, CmsGroupUser.USER == self.USER).first()
        return item

    def get_all(self):
        item = self.db_session.query(CmsGroupUser).filter(
            CmsGroupUser.GROUP == self.GROUP, CmsGroupUser.USER == self.USER).all()
        return item

    @classmethod
    def get_by_group_and_user(cls, group, user):
        item = cls.db_session.query(CmsGroupUser).filter(
            CmsGroupUser.GROUP == group, CmsGroupUser.USER == user).first()
        return item