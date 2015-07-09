__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from reindeer.sys.base_db_model import InfoTableModel, new_alchemy_encoder
import json


class SysGroup(InfoTableModel):
    __tablename__ = 'RA_SYS_GROUP'
    NAME = Column(String(100))
    DES = Column(String(1000))

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
    def delete(cls, id):
        items = cls.db_session.query(SysGroup).filter(SysGroup.ID == id)
        if items.count() < 1:
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
        item = cls.db_session.query(SysGroup).all()
        return item

    @classmethod
    def get_all_json(cls):
        r_json = []
        items = SysGroup.get_all()
        for item in items:
            r_json.append(item)
        return json.dumps(r_json, cls=new_alchemy_encoder(), check_circular=False)