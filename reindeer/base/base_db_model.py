__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, or_
from datetime import datetime
import uuid
import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from reindeer.sys import constants

# 以下是不提供默认字段的普通表基类，因为有关系的表必须来自同一个Base，所以这个类暂时不推荐用
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


def to_json(items):
    items = not isinstance(items, list) and [items] or items
    r_json = []
    for item in items:
        r_json.append(item)
    return json.dumps(r_json, cls=new_alchemy_encoder(), check_circular=False)


def to_page(items_query, key_word, start, end, sort_col, sort_dir, *search_cols, **sort_cols):
    page = {"total": items_query.count()}
    search = []
    for col in search_cols:
        search.append(col.like("%" + key_word + "%"))
    item = items_query.filter(or_(*search))
    page["search_total"] = item.count()
    order_by = None
    if not sort_col == '0':
        order_by = sort_cols[sort_col].desc() if sort_dir == 'desc' else sort_cols[sort_col].asc()
    if order_by is not None:
        item = item.order_by(order_by)
    if end > start:
        item = item.slice(start, end)
    page["data"] = item.all()
    return page