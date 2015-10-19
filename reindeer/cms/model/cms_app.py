__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

from sqlalchemy import Column, String
from reindeer.base.base_db_model import InfoTableModel
from reindeer.cms import constants


class CmsApp(InfoTableModel):
    __tablename__ = 'RA_CMS_APP'
    NAME = Column(String(100))
    CODE = Column(String(100), unique=True)
    KEY = Column(String(100), unique=True)
    TYPE = Column(String(2), default=constants.app_type_default)
    CONTROL = Column(String(100), default=constants.app_control_default)
    DES = Column(String(1000))
    ICON_TYPE = Column(String(1), default=constants.icon_client)
    ICON = Column(String(200))
    THEME = Column(String(50))

    @classmethod
    def add(cls, name=None, code=None, key=None, des=None, icon_type=None, icon=None, theme=None):
        app = CmsApp(NAME=name, CODE=code, KEY=key, DES=des, ICON_TYPE=icon_type, ICON=icon, THEME=theme)
        cls.db_session.add(app)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (app.ID):
            return 0
        else:
            return 1