from abc import ABC, abstractmethod

class FactoryService(ABC):

    @abstractmethod
    def query_city_repository(self) -> "CityRepositoryQuery":
        ...
