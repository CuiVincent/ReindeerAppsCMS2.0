__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String, ForeignKey
from reindeer.base.base_db_model import InfoTableModel


class CmsGroupAction(InfoTableModel):
    __tablename__ = 'RA_SYS_GROUP_ACTION'
    GROUP = Column(String(50), ForeignKey('RA_CMS_GROUP.ID', ondelete='CASCADE', onupdate='CASCADE'))
    ACTION = Column(String(50), ForeignKey('RA_SYS_ACTION.ID', ondelete='CASCADE', onupdate='CASCADE'))

    @classmethod
    def add(cls, group, action):
        action = not isinstance(action, list) and [action] or action
        group = not isinstance(group, list) and [group] or group
        for a in action:
            for g in group:
                group_action = CmsGroupAction(ACTION=a, GROUP=g)
                if not group_action.get():
                    cls.db_session.add(group_action)
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def delete_by_group_and_add(cls, group, action):
        group = not isinstance(group, list) and [group] or group
        for g in group:
            items = cls.db_session.query(CmsGroupAction).filter(CmsGroupAction.GROUP == g)
            if items:
                items.delete()
        if not action or action is '' or (isinstance(action, list) and len(action) is 1 and action[0] is ''):
            return 0
        try:
            return CmsGroupAction.add(group, action)
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def delete(cls, group, action):
        action = not isinstance(action, list) and [action] or action
        group = not isinstance(group, list) and [group] or group
        for a in action:
            for g in group:
                items = cls.db_session.query(CmsGroupAction).filter(CmsGroupAction.GROUP == g,
                                                                    CmsGroupAction.ACTION == a)
                if items:
                    items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    def get(self):
        item = self.db_session.query(CmsGroupAction).filter(
            CmsGroupAction.GROUP == self.GROUP, CmsGroupAction.ACTION == self.ACTION).first()
        return item

    @classmethod
    def get_by_group_and_action(cls, group, action):
        item = cls.db_session.query(CmsGroupAction).filter(
            CmsGroupAction.GROUP == group, CmsGroupAction.ACTION == action).first()
        return item