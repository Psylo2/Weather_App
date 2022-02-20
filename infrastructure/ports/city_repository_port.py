from typing import Union, Dict

from infrastructure.adapters.persistence_adapter import repository
from infrastructure.ports.services import CityRepositoryPortService


class CityRepository(repository.Model, CityRepositoryPortService):
    __tablename__ = 'city'
    id = repository.Column(repository.Integer, primary_key=True, autoincrement=True)
    name = repository.Column(repository.String(30), unique=True, nullable=False)

    def __init__(self, id: Union[int, None], name: str):
        self.id = id
        self.name = name

    def add_to_repository(self) -> None:
        repository.session.add(self)
        repository.session.commit()

    def remove_from_repository(self) -> None:
        repository.session.delete(self)
        repository.session.commit()

    def dict(self) -> Dict:
        return {"id": self.id,
                "name": self.name}
