__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import uuid
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from reindeer.base.base_db_model import InfoTableModel, to_json
from reindeer.cms.model.cms_group_action import CmsGroupAction
from reindeer.cms.model.cms_group_user import CmsGroupUser
from reindeer.cms.model.cms_group import CmsGroup
from reindeer.cms import constants


class CmsLayout(InfoTableModel):
    __tablename__ = 'RA_CMS_LAYOUT'
    NAME = Column(String(100))
    DES = Column(String(1000))
    CODE = Column(String(100), unique=True)
    COLOR = Column(String(1000))
    TRANS = Column(String(50), default=constants.layout_trans_default)
    PARENT = Column(String(50), default=constants.layout_root)
    LOCATION = Column(String(500))

    @classmethod
    def add(cls, name=None, des=None, code=None):
        layout = CmsLayout(NAME=name, DES=des, CODE=code)
        # if not str(layout.PARENT) == constants.layout_root:
        # if not cls.get_by_id(layout.PARENT):
        #         return err
        cls.db_session.add(layout)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (layout.ID):
            return 0
        else:
            return 1