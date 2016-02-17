__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from reindeer.base.base_db_model import InfoTableModel, to_json, to_page
from reindeer.cms.model.cms_group_user import CmsGroupUser


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
    def get_page_by_c_user(cls, c_user, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': CmsGroup.NAME,
            u'2': CmsGroup.DES,
            u'3': CmsGroup.C_DATE
        }
        search_cols = (
            CmsGroup.NAME,
            CmsGroup.DES
        )
        return to_page(cls.db_session.query(CmsGroup).filter(CmsGroup.C_USER == c_user), key_word, start, end, sort_col,
                       sort_dir, *search_cols,
                       **sort_cols)

    @classmethod
    def get_page_json_by_c_user(cls, c_user, key_word, start, end, sort_col, sort_dir):
        page = CmsGroup.get_page_by_c_user(c_user, key_word, start, end, sort_col, sort_dir)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_joined_user_and_c_user(cls, uid, c_user, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': CmsGroup.NAME
        }
        search_cols = (
            CmsGroup.NAME,
        )
        query = cls.db_session.query(CmsGroup).join(CmsGroupUser).filter(CmsGroupUser.USER == uid)
        query = query.filter(CmsGroup.C_USER == c_user)
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_unjoined_user_and_c_user(cls, uid, c_user, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': CmsGroup.NAME
        }
        search_cols = (
            CmsGroup.NAME,
        )
        sub = cls.db_session.query(CmsGroup.ID).join(CmsGroupUser).filter(
            CmsGroupUser.USER == uid).subquery()
        query = cls.db_session.query(CmsGroup).filter(~CmsGroup.ID.in_(sub))
        query = query.filter(CmsGroup.C_USER == c_user)
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page
