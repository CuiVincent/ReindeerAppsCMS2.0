__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import uuid
from sqlalchemy import Column, String
from reindeer.base.base_db_model import InfoTableModel, to_json
from reindeer.cms import constants


class CmsApp(InfoTableModel):
    __tablename__ = 'RA_CMS_APP'
    NAME = Column(String(100))
    CODE = Column(String(100))
    KEY = Column(String(100))
    TYPE = Column(String(2), default=constants.app_type_default)
    CONTROL = Column(String(100),
                     default=constants.app_control_login + '&' + constants.app_control_action + '&' + constants.app_control_data)
    DES = Column(String(1000))
    ICON_TYPE = Column(String(1), default=constants.icon_client)
    ICON = Column(String(200))

    @classmethod
    def add(cls, name=None, code=None, key=None, ctrl=None, des=None, icon_type=None, icon=None, c_user=None):
        app = CmsApp(NAME=name, CODE=code, KEY=key, CONTROL=ctrl, DES=des, ICON_TYPE=icon_type, ICON=icon)
        if c_user:
            app.set_c_user(c_user)
        cls.db_session.add(app)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (app.ID):
            return 0
        else:
            return 1

    @classmethod
    def delete(cls, id):
        items = cls.db_session.query(CmsApp).filter(CmsApp.ID == id)
        if not items:
            return 11201
        items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    @classmethod
    def get_by_id(cls, id):
        item = cls.db_session.query(CmsApp).filter(CmsApp.ID == id).first()
        return item

    @classmethod
    def get_tree(cls, base_url):
        items = cls.db_session.query(CmsApp).all()
        apps = []
        for item in items:
            apps.append(
                {'id': item.ID, 'v_id': str(uuid.uuid1()), 'name': item.NAME,
                 'url': base_url + '/' + item.ID,
                 'icon_type': item.ICON_TYPE, 'icon': item.ICON, 'children': None, 'scale_script': None})
        return apps

    @classmethod
    def get_all(cls):
        return cls.db_session.query(CmsApp).order_by(
            CmsApp.C_DATE.desc()).all()

    @classmethod
    def get_all_json(cls):
        return to_json(CmsApp.get_all())