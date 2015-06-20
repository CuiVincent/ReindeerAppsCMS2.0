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
    def add(cls, name, des):
        group = SysGroup(NAME=name, DES=des)
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