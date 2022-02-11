from abc import ABC, abstractmethod
from repositories import CityRepository

class FactoryService(ABC):

    @abstractmethod
    def get_city_repository(self) -> CityRepository:
        ...


class Factory(FactoryService):
    def __init__(self):
        self._city_repository = None

    def get_city_repository(self) -> CityRepository:
        if not self._city_repository:
            self._city_repository = CityRepository
        return self._city_repository
