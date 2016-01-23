__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from reindeer.base.base_db_model import InfoTableModel, to_json
from reindeer.cms.model.cms_group_user import CmsGroupUser
from reindeer.cms.model.cms_group_action import CmsGroupAction


class CmsGroup(InfoTableModel):
    __tablename__ = 'RA_CMS_GROUP'
    NAME = Column(String(100))
    DES = Column(String(1000))
    users = relationship('CmsUser', secondary='RA_CMS_GROUP_USER')
    actions = relationship('CmsAction', secondary='RA_CMS_GROUP_ACTION')

    @classmethod
    def add(cls, name, des, c_user=None):
        group = CmsGroup(NAME=name, DES=des)
        if c_user:
            group.set_c_user(c_user)
        cls.db_session.add(group)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (group.ID):
            return 0
        else:
            return 1

    @classmethod
    def add_and_get(cls, name, des, c_user=None):
        group = CmsGroup(NAME=name, DES=des)
        if c_user:
            group.set_c_user(c_user)
        cls.db_session.add(group)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (group.ID):
            return group
        else:
            return None

    @classmethod
    def delete(cls, id):
        items = cls.db_session.query(CmsGroup).filter(CmsGroup.ID == id)
        if not items:
            return 11101
        items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def update(cls, id, name, des):
        items = cls.db_session.query(CmsGroup).filter(CmsGroup.ID == id)
        if items.count() < 1:
            return 11102
        update = {
            CmsGroup.NAME: name,
            CmsGroup.DES: des,
        }
        items.update(update)
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def get_all(cls):
        return cls.db_session.query(CmsGroup).all()

    @classmethod
    def get_all_json(cls):
        return to_json(CmsGroup.get_all())

    @classmethod
    def get_json_by_joined_user(cls, uid):
        items = cls.db_session.query(CmsGroup).join(CmsGroupUser).filter(
            CmsGroupUser.USER == uid).all()
        return to_json(items)

    @classmethod
    def get_json_by_unjoined_user(cls, uid):
        sub = cls.db_session.query(CmsGroup.ID).join(CmsGroupUser).filter(
            CmsGroupUser.USER == uid).subquery()
        items = cls.db_session.query(CmsGroup).filter(~CmsGroup.ID.in_(sub)).all()
        return to_json(items)

    @classmethod
    def get_json_by_joined_action(cls, aid):
        items = cls.db_session.query(CmsGroup).join(CmsGroupAction).filter(
            CmsGroupAction.ACTION == aid).all()
        return to_json(items)

    @classmethod
    def get_json_by_unjoined_action(cls, aid):
        sub = cls.db_session.query(CmsGroup.ID).join(CmsGroupAction).filter(
            CmsGroupAction.ACTION == aid).subquery()
        items = cls.db_session.query(CmsGroup).filter(~CmsGroup.ID.in_(sub)).all()
        return to_json(items)