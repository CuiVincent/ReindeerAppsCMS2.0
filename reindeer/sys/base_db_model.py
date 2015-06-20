__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from reindeer.sys import constants

# 以下是不提供默认字段的普通表基类
NormalTableModel = declarative_base(name='NormalTableModel')

# 以下是提供ID、创建信息等默认字段的信息表基类
InfoTableModel = declarative_base(name='InfoTableModel')
InfoTableModel.ID = Column(String(50), primary_key=True)
InfoTableModel.C_USER = Column(String(50), default=constants.str_user_unknown)
InfoTableModel.C_DATE = Column(DateTime, default=datetime.now())

original_init = InfoTableModel.__init__


def info_table_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    if not self.ID:
        self.ID = uuid.uuid1()
    self.C_DATE = datetime.now()


InfoTableModel.__init__ = info_table_init


def set_c_user(self, c_user):
    self.C_USER = c_user


InfoTableModel.set_c_user = set_c_user


# 以下是一些通用方法
def new_alchemy_encoder():
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    data = obj.__getattribute__(field)
                    try:
                        if isinstance(data, datetime):
                            data = data.strftime('%Y-%m-%d %H:%M:%S')
                        json.dumps(data)  # this will fail on non-encodable values, like other classes
                        fields[field] = data
                    except TypeError:
                        pass
                        # fields[field] = None
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder