__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from reindeer.base.base_db_model import InfoTableModel


class CmsApp(InfoTableModel):
    __tablename__ = 'RA_CMS_APP'
    NAME = Column(String(100))
    PACKAGE_NAME = Column(String(100), unique=True)
    DES = Column(String(1000))
    ICON_TYPE = Column(String(1), default='1')
    ICON = Column(String(200))
    THEME = Column(String(50))

    @classmethod
    def add(cls, name=None, package_name=None, des=None, icon_type=None, icon=None, theme=None):
        app = CmsApp(NAME=name, PACKAGE_NAME=package_name, DES=des, ICON_TYPE=icon_type, ICON=icon, THEME=theme)
        cls.db_session.add(app)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (app.ID):
            return 0
        else:
            return 1