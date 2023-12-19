from sqlalchemy.exc import OperationalError

from app.business.repository.interface import FilterManager, CreateManager, UpdateManager

from config.db_connection import get_db


class Repository(FilterManager, CreateManager, UpdateManager):
    def __init__(self, entity):
        self._entity = entity

    def filter(self, kwargs: dict):
        try:
            with get_db() as db:
                _instance = db.query(self._entity).filter_by(**kwargs)
                return _instance
        except OperationalError as e:
            print("OperationalError filter dao_repository.py -> ", e)
            with get_db() as db:
                db.rollback()
            raise e
        except Exception as e:
            print("Exception filter dao_repository.py -> ", e)
            with get_db() as db:
                db.rollback()
            raise e

    def create(self, data: dict):
        try:
            with get_db() as db:
                _instance = self._entity(**data)
                db.add(_instance)
                db.commit()
                return _instance

        except Exception as e:
            print("Exception create dao_repository.py -> ", e)
            with get_db() as db:
                db.rollback()
            raise e

    def update(self, filters, kwargs):
        """."""
        try:
            with get_db() as db:
                db.query(self._entity).filter_by(**filters).update(kwargs)
                db.commit()
                return self.filter(filters).first()
        except OperationalError as e:
            print("OperationalError update dao_repository.py -> ", e)
            with get_db() as db:
                db.rollback()
            raise e
        except Exception as e:
            print("Exception update dao_repository.py -> ", e)
            with get_db() as db:
                db.rollback()
            raise e
