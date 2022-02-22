from abc import ABC, abstractmethod

class CityUseCase(ABC):

    @abstractmethod
    def register_city(self, city_name: str) -> None:
        ...

    @abstractmethod
    def remove_city(self, _id: int) -> bool:
        ...
        
    @abstractmethod
    def get_all_cities_current_weather(self) -> List[Dict]:
        ...
