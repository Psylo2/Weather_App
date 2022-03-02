from abc import ABC, abstractmethod
from typing import Dict, List, Union


class CityRepositoryQueryService(ABC):

    @abstractmethod
    def add_city(self, city_data: Dict) -> "CityRepository":
        ...

    @abstractmethod
    def remove_city(self, city: "CityRepository") -> None:
        ...

    @abstractmethod
    def get_all_cities(self) -> List[Dict]:
        ...

    @abstractmethod
    def get_city_by_id(self, id: int) -> Union["CityRepository", None]:
        ...

    @abstractmethod
    def get_all_cities_name_list(self) -> List["CityRepository"]:
        ...
