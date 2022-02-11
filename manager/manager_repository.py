from flask_sqlalchemy import SQLAlchemy

from manager.services import RepositoryService


class RepositoryManager(RepositoryService):
    def __init__(self):
        self._db = SQLAlchemy()

    @property
    def db(self):
        return self._db


repository: RepositoryManager = RepositoryManager()
