__author__ = 'cuizhe01'
from app_settings import db_settings
from reindeer.base.base_db_model import InfoTableModel, NormalTableModel
from reindeer.base.util.database_util import DatabaseInstance, DatabaseUtil

if __name__ == "__main__":
    db_instance = DatabaseInstance(db_settings, [InfoTableModel, NormalTableModel])
    DatabaseUtil.init(db_instance)