__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String, Integer, or_
from sqlalchemy.exc import IntegrityError
from reindeer.util.common_util import to_md5
from reindeer.sys.base_db_model import InfoTableModel, new_alchemy_encoder
from reindeer.sys.exceptions import BusinessRuleException
from reindeer.sys import constants
import json


class SysUser(InfoTableModel):
    __tablename__ = 'RA_SYS_USER'
    CODE = Column(String(100), unique=True)
    NAME = Column(String(100))
    PASSWORD = Column(String(100))
    STATUS = Column(String(1), default=constants.user_status_normal)

    @classmethod
    def add(cls, user_code, user_name, pass_wd, status=constants.user_status_normal, c_user=None):
        user = SysUser(CODE=user_code, NAME=user_name, PASSWORD=to_md5(pass_wd) if pass_wd else '', STATUS=status)
        if c_user:
            user.set_c_user(c_user)
        cls.db_session.add(user)
        try:
            cls.db_session.commit()
        except IntegrityError:
            cls.db_session.rollback()
            raise BusinessRuleException(1051)
            # 先回滚再抛出异常，否则回滚不会执行
        except:
            cls.db_session.rollback()
        if (user.ID):
            return user
        else:
            return None

    @classmethod
    def delete(cls, user_ID):
        items = cls.db_session.query(SysUser).filter(SysUser.ID == user_ID)
        if items.count() < 1:
            return False
        items.delete()
        try:
            cls.db_session.commit()
            return True
        except:
            cls.db_session.rollback()
            return False

    @classmethod
    def update(cls, user_ID, user_name, user_status):
        items = cls.db_session.query(SysUser).filter(SysUser.ID == user_ID)
        if items.count() < 1:
            return False
        update = {
            SysUser.NAME: user_name,
            SysUser.STATUS: user_status,
        }
        items.update(update)
        try:
            cls.db_session.commit()
            return True
        except:
            cls.db_session.rollback()
            return False

    @classmethod
    def get_by_code(cls, user_code):
        item = cls.db_session.query(SysUser).filter(SysUser.CODE == user_code).first()
        return item

    @classmethod
    def get_by_id(cls, user_ID):
        item = cls.db_session.query(SysUser).filter(SysUser.ID == user_ID).first()
        return item

    @classmethod
    def get_all(cls):
        return cls.db_session.query(SysUser).all()

    @classmethod
    def get_all_json(cls):
        r_json = []
        items = SysUser.get_all()
        for item in items:
            r_json.append(item)
        return json.dumps(r_json, cls=new_alchemy_encoder(), check_circular=False)

    @classmethod
    def get_all_count(cls):
        return cls.db_session.query(SysUser).count()

    @classmethod
    def get_slice(cls, like, start, stop, sort_col, sort_dir):
        sort_cols = {
            u'1': SysUser.CODE,
            u'2': SysUser.NAME,
            u'3': SysUser.STATUS,
            u'4': SysUser.C_USER,
            u'5': SysUser.C_DATE
        }
        order_by = -sort_cols[sort_col] if sort_dir == 'desc' else sort_cols[sort_col]
        item = cls.db_session.query(SysUser).filter(
            or_(SysUser.CODE.like("%" + like + "%"), SysUser.NAME.like("%" + like + "%"),
                SysUser.C_USER.like("%" + like + "%")))
        if order_by is not None:
            item = item.order_by(order_by)
        if stop - start >= 0:
            item = item.slice(start, stop)
        return item.all()

    @classmethod
    def get_slice_json(cls, like, start, stop, sort_col, sort_dir):
        r_json = []
        items = SysUser.get_slice(like, start, stop, sort_col, sort_dir)
        for item in items:
            r_json.append(item)
        return json.dumps(r_json, cls=new_alchemy_encoder(), check_circular=False)

    @classmethod
    def get_slice_count(cls, like):
        return cls.db_session.query(SysUser).filter(
            or_(SysUser.CODE.like("%" + like + "%"), SysUser.NAME.like("%" + like + "%"),
                SysUser.C_USER.like("%" + like + "%"))).count()