from abc import ABC, abstractmethod
from typing import Union, Dict, List


class CityHandlerService(ABC):

    @abstractmethod
    def api_url(self) -> str:
        ...

    @abstractmethod
    def _get_weather_api_params(self, city_name: str) -> Dict:
        ...

    @abstractmethod
    def _request_weather_info(self, city_name: str) -> Dict:
        ...

    @abstractmethod
    def _get_day_time_description(self, hour: int) -> str:
        ...

    @abstractmethod
    def _get_local_timezone_hour(self, info: Dict) -> int:
        ...

    @abstractmethod
    def _get_weather_report(self, city: Dict, info: Dict, local_hour: int) -> Dict:
        ...

    @abstractmethod
    def get_weather(self, city: Dict) -> Union[Dict, None]:
        ...

    @abstractmethod
    def get_all_cities_from_repository(self) -> List[Dict]:
        ...

    @abstractmethod
    def get_city_by_id(self, id: int) -> Dict:
        ...

    @abstractmethod
    def get_all_cities_current_weather(self) -> List[Dict]:
        ...
