from abc import ABC, abstractmethod

class CityUseCase(ABC):

    @abstractmethod
    def register_city(self, city: "CityEntity") -> None:
        ...

    @abstractmethod
    def remove_city(self, _id: int) -> bool:
        ...
