__author__ = 'CuiVincent'
# -*- coding: utf8 -*-

import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from reindeer.base.base_db_model import InfoTableModel, to_json
from reindeer.cms.model.cms_group_action import CmsGroupAction
from reindeer.cms.model.cms_group_user import CmsGroupUser
from reindeer.cms.model.cms_group import CmsGroup
from reindeer.cms import constants


class CmsAction(InfoTableModel):
    __tablename__ = 'RA_CMS_ACTION'
    NAME = Column(String(100))
    TYPE = Column(String(2), default=constants.action_type_page)
    DES = Column(String(1000))
    PARENT = Column(String(50), default=constants.action_root)
    LOG = Column(String(1), default='1')
    SORT = Column(Integer)
    ICON_TYPE = Column(String(1), default=constants.icon_client)
    ICON = Column(String(200))
    THEME = Column(String(50))
    APP = Column(String(50))
    groups = relationship('CmsGroup', secondary='RA_CMS_GROUP_ACTION')

    @classmethod
    def add(cls, name=None, type=None, des=None, parent=None, log=None, sort=None, icon_type=None, icon=None,
            theme=None, app=None):
        action = CmsAction(NAME=name, TYPE=type, DES=des, PARENT=parent, LOG=log, SORT=sort,
                           ICON_TYPE=icon_type,
                           ICON=icon, THEME=theme, APP=app)
        if not str(action.PARENT) == constants.action_root:
            if not cls.get_by_id(action.PARENT):
                return 11151
        cls.db_session.add(action)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (action.ID):
            return 0
        else:
            return 1

    @classmethod
    def add_and_get(cls, name=None, type=None, url=None, des=None, parent=None, log=None, sort=None, icon_type=None,
                    icon=None):
        action = CmsAction(NAME=name, TYPE=type, URL=url, DES=des, PARENT=parent, LOG=log, SORT=sort,
                           ICON_TYPE=icon_type,
                           ICON=icon)
        if not str(action.PARENT) == constants.action_root:
            if not cls.get_by_id(action.PARENT):
                return None
        cls.db_session.add(action)
        try:
            cls.db_session.commit()
        except:
            cls.db_session.rollback()
        if (action.ID):
            return action
        else:
            return None

    @classmethod
    def delete(cls, id):
        items = cls.db_session.query(CmsAction).filter(CmsAction.ID == id)
        if not items:
            return 11152
        if CmsAction.get_by_parent(items.first().ID):
            return 11153
        items.delete()
        try:
            cls.db_session.commit()
            return 0
        except:
            cls.db_session.rollback()
            return 1

    # @classmethod
    # def update(cls, id, name, des, sort, icon):
    #     items = cls.db_session.query(CmsAction).filter(CmsAction.ID == id)
    #     if items.count() < 1:
    #         return 11154
    #     update = {
    #         CmsAction.NAME: name,
    #         CmsAction.DES: des,
    #         CmsAction.SORT: sort,
    #         CmsAction.ICON: icon
    #     }
    #     items.update(update)
    #     try:
    #         cls.db_session.commit()
    #         return 0
    #     except:
    #         cls.db_session.rollback()
    #         return 1

    @classmethod
    def get_by_id(cls, id):
        item = cls.db_session.query(CmsAction).filter(CmsAction.ID == id).first()
        return item

    @classmethod
    def get_json_by_id(cls, id):
        return to_json(CmsAction.get_by_id(id))

    @classmethod
    def get_by_parent(cls, pid):
        item = cls.db_session.query(CmsAction).filter(CmsAction.PARENT == pid).first()
        return item

    @classmethod
    def get_parent_by_id(cls, id):
        item = CmsAction.get_by_id(id)
        if not item:
            return None
        else:
            parent = CmsAction.get_by_id(item.PARENT)
        return parent

    @classmethod
    def get_tree_by_user_and_parent(cls, user_id, parent, type):
        items = cls.db_session.query(CmsAction).join(CmsGroupAction).join(CmsGroup).join(CmsGroupUser).filter(
            CmsGroupUser.USER == user_id, CmsAction.PARENT == parent, CmsAction.TYPE == type).order_by(
            CmsAction.SORT.asc()).all()
        actions = []
        for item in items:
            actions.append(
                {'id': item.ID, 'v_id': str(uuid.uuid1()), 'name': item.NAME, 'url': item.URL,
                 'icon_type': item.ICON_TYPE, 'icon': item.ICON,
                 'children': CmsAction.get_tree_by_user_and_parent(user_id, item.ID, type)})
        return actions

    @classmethod
    def get_tree_by_parent(cls, parent, type):
        items = cls.db_session.query(CmsAction).filter(CmsAction.PARENT == parent, CmsAction.TYPE == type).order_by(
            CmsAction.SORT.asc()).all()
        actions = []
        for item in items:
            actions.append(
                {'id': item.ID, 'name': item.NAME, 'url': item.URL,
                 'icon_type': item.ICON_TYPE, 'icon': item.ICON,
                 'children': CmsAction.get_tree_by_parent(item.ID, type)})
        return actions

    @classmethod
    def get_ratree_by_parent(cls, parent, type):
        items = cls.db_session.query(CmsAction).filter(CmsAction.PARENT == parent, CmsAction.TYPE == type).order_by(
            CmsAction.SORT.asc()).all()
        actions = []
        for item in items:
            actions.append(
                {'id': item.ID, 'title': item.NAME,
                 'icon_type': item.ICON_TYPE, 'icon': item.ICON,
                 'children': CmsAction.get_ratree_by_parent(item.ID, type)})
        return actions

    @classmethod
    def get_ratree_checked_by_group(cls, type, gid):
        items = cls.db_session.query(CmsAction.ID).join(CmsGroupAction).filter(
            CmsAction.TYPE == type, CmsGroupAction.GROUP == gid).all()
        actions = []
        for item in items:
            actions.append(
                {'id': item.ID})
        return actions