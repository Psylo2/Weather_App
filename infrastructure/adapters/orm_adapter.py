from flask_sqlalchemy import SQLAlchemy

class ORMAdapter:

    def __new__(cls, *args, **kwargs):
        return SQLAlchemy()
