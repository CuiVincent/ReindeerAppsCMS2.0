__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from reindeer.base.util.common_util import to_md5
from reindeer.base.base_db_model import InfoTableModel, to_json, to_page
from reindeer.sys import constants
from reindeer.sys.model.sys_group_user import SysGroupUser


class SysUser(InfoTableModel):
    __tablename__ = 'RA_SYS_USER'
    CODE = Column(String(100), unique=True)
    NAME = Column(String(100))
    PASSWORD = Column(String(100))
    STATUS = Column(String(1), default=constants.user_status_normal)
    groups = relationship('SysGroup', secondary='RA_SYS_GROUP_USER')

    @classmethod
    def add(cls, code, name, pass_wd, status=constants.user_status_normal, c_user=None):
        user = SysUser(CODE=code, NAME=name, PASSWORD=to_md5(pass_wd) if pass_wd else '', STATUS=status)
        if c_user:
            user.set_c_user(c_user)
        cls.db_session.add(user)
        try:
            cls.db_session.commit()
        except IntegrityError:
            cls.db_session.rollback()
            return 1051
            # 先回滚再抛出异常，否则回滚不会执行
        except:
            cls.db_session.rollback()
        if (user.ID):
            return 0
        else:
            return 1

    @classmethod
    def add_and_get(cls, code, name, pass_wd, status=constants.user_status_normal, c_user=None):
        user = SysUser(CODE=code, NAME=name, PASSWORD=to_md5(pass_wd) if pass_wd else '', STATUS=status)
        if c_user:
            user.set_c_user(c_user)
        cls.db_session.add(user)
        try:
            cls.db_session.commit()
        except IntegrityError:
            cls.db_session.rollback()
            return None
        except:
            cls.db_session.rollback()
        if (user.ID):
            return user
        else:
            return None

    @classmethod
    def delete(cls, id):
        items = cls.db_session.query(SysUser).filter(SysUser.ID == id)
        if not items.count():
            return 1052
        items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def update(cls, id, name, status):
        items = cls.db_session.query(SysUser).filter(SysUser.ID == id)
        if items.count() < 1:
            return 1053
        update = {
            SysUser.NAME: name,
            SysUser.STATUS: status,
        }
        items.update(update)
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def get_by_code(cls, user_code):
        item = cls.db_session.query(SysUser).filter(SysUser.CODE == user_code).first()
        return item

    @classmethod
    def get_by_id(cls, id):
        item = cls.db_session.query(SysUser).filter(SysUser.ID == id).first()
        return item

    @classmethod
    def get_all(cls):
        return cls.db_session.query(SysUser).all()

    @classmethod
    def get_all_json(cls):
        items = SysUser.get_all()
        return to_json(items)

    @classmethod
    def get_page(cls, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysUser.CODE,
            u'2': SysUser.NAME,
            u'3': SysUser.STATUS,
            u'4': SysUser.C_USER,
            u'5': SysUser.C_DATE
        }
        search_cols = (
            SysUser.CODE,
            SysUser.NAME,
            SysUser.C_USER
        )
        return to_page(cls.db_session.query(SysUser), key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)

    @classmethod
    def get_page_json(cls, key_word, start, stop, sort_col, sort_dir):
        page = SysUser.get_page(key_word, start, stop, sort_col, sort_dir)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_joined_groupid(cls, gid, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysUser.CODE,
            u'2': SysUser.NAME
        }
        search_cols = (
            SysUser.CODE,
            SysUser.NAME
        )
        query = cls.db_session.query(SysUser).join(SysGroupUser).filter(SysGroupUser.GROUP == gid)
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page

    @classmethod
    def get_page_json_by_unjoined_groupid(cls, gid, key_word, start, end, sort_col, sort_dir):
        sort_cols = {
            u'1': SysUser.CODE,
            u'2': SysUser.NAME
        }
        search_cols = (
            SysUser.CODE,
            SysUser.NAME
        )
        sub = cls.db_session.query(SysUser.ID).join(SysGroupUser).filter(SysGroupUser.GROUP == gid).subquery()
        query = cls.db_session.query(SysUser).filter(~SysUser.ID.in_(sub))
        page = to_page(query, key_word, start, end, sort_col, sort_dir, *search_cols,
                       **sort_cols)
        page["data"] = to_json(page["data"])
        return page