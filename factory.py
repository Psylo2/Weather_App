from abc import ABC, abstractmethod
from repositories.controllers import CityRepositoryController

class FactoryService(ABC):

    @abstractmethod
    def get_city_repository(self) -> CityRepositoryController:
        ...


class Factory(FactoryService):
    def __init__(self):
        self._city_repository = None

    def get_city_repository(self) -> CityRepositoryController:
        if not self._city_repository:
            self._city_repository = CityRepositoryController()
        return self._city_repository
