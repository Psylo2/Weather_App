from typing import Union, Dict

from manager.manager_repository import repository
from repositories.services import RepositoryService

class CityRepository(repository.db.Model, RepositoryService):
    __tablename__ = 'city'
    id = repository.db.Column(repository.db.Integer, primary_key=True, autoincrement=True)
    name = repository.db.Column(repository.db.String(30), unique=True, nullable=False)

    def __init__(self, id: Union[int, None], name: str):
        self.id = id
        self.name = name

    def add_to_repository(self) -> None:
        repository.db.session.add(self)
        repository.db.session.commit()

    def remove_from_repository(self) -> None:
        repository.db.session.delete(self)
        repository.db.session.commit()

    def dict(self) -> Dict:
        return {"id": self.id,
                "name": self.name}

