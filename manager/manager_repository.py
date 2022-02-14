from flask_sqlalchemy import SQLAlchemy


class RepositoryManager:

    def __new__(cls, *args, **kwargs):
        return SQLAlchemy()


repository = RepositoryManager()
