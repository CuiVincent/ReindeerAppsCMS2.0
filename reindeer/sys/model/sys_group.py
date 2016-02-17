__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from reindeer.base.base_db_model import InfoTableModel, to_json, to_page
from reindeer.sys.model.sys_group_user import SysGroupUser
from reindeer.sys.model.sys_group_action import SysGroupAction


class SysGroup(InfoTableModel):
    __tablename__ = 'RA_SYS_GROUP'
    NAME = Column(String(100))
    DES = Column(String(1000))
    users = relationship('SysUser', secondary='RA_SYS_GROUP_USER')
    actions = relationship('SysAction', secondary='RA_SYS_GROUP_ACTION')

    @classmethod
    def add(cls, name, des, c_user=None):
        group = SysGroup(NAME=name, DES=des)
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
        group = SysGroup(NAME=name, DES=des)
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
        items = cls.db_session.query(SysGroup).filter(SysGroup.ID == id)
        if not items:
            return 1101
        items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def update(cls, id, name, des):
        items = cls.db_session.query(SysGroup).filter(SysGroup.ID == id)
        if items.count() < 1:
            return 1102
        update = {
            SysGroup.NAME: name,
            SysGroup.DES: des,
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
        return cls.db_session.query(SysGroup).all()

    @classmethod
    def get_all_json(cls):
        return to_json(SysGroup.get_all())

    @classmethod
    def get_page(cls, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysGroup.NAME,
            u'2': SysGroup.DES,
            u'3': SysGroup.C_USER,
            u'4': SysGroup.C_DATE
        }
        search_cols = (
            SysGroup.NAME,
            SysGroup.DES,
            SysGroup.C_USER
        )
        return to_page(cls.db_session.query(SysGroup), key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)

    @classmethod
    def get_page_json(cls, key_word, start, end, sort_col, sort_dir):
        page = SysGroup.get_page(key_word, start, end, sort_col, sort_dir)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_joined_user(cls, uid, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysGroup.NAME
        }
        search_cols = (
            SysGroup.NAME,
        )
        query = cls.db_session.query(SysGroup).join(SysGroupUser).filter(SysGroupUser.USER == uid)
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_unjoined_user(cls, uid, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysGroup.NAME
        }
        search_cols = (
            SysGroup.NAME,
        )
        sub = cls.db_session.query(SysGroup.ID).join(SysGroupUser).filter(
            SysGroupUser.USER == uid).subquery()
        query = cls.db_session.query(SysGroup).filter(~SysGroup.ID.in_(sub))
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_joined_action(cls, aid, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysGroup.NAME
        }
        search_cols = (
            SysGroup.NAME,
        )
        query = cls.db_session.query(SysGroup).join(SysGroupAction).filter(
            SysGroupAction.ACTION == aid)
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_unjoined_action(cls, aid, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysGroup.NAME
        }
        search_cols = (
            SysGroup.NAME,
        )
        sub = cls.db_session.query(SysGroup.ID).join(SysGroupAction).filter(
            SysGroupAction.ACTION == aid).subquery()
        query = cls.db_session.query(SysGroup).filter(~SysGroup.ID.in_(sub))
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page