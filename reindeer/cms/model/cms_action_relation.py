__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String, Integer, ForeignKey
from reindeer.base.base_db_model import InfoTableModel


class CmsActionRelation(InfoTableModel):
    __tablename__ = 'RA_CMS_ACTION_RELATION'
    FROM = Column(String(50), ForeignKey('RA_CMS_ACTION.ID', ondelete='CASCADE', onupdate='CASCADE'))
    TO = Column(String(50), ForeignKey('RA_CMS_ACTION.ID', ondelete='CASCADE', onupdate='CASCADE'))
    SORT = Column(Integer)
