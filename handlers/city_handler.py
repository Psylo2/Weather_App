import os

import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Union

from handlers.services import CityHandlerService
from usecases.city_usecase import CityUseCase
from models import CityEntity


class CityHandler(CityUseCase, CityHandlerService):

    def __init__(self, factory):
        self._factory = factory
        self._city_repository = factory.get_city_repository()

    @property
    def api_url(self) -> str:
        return 'https://api.openweathermap.org/data/2.5/weather'

    def _get_weather_api_params(self, city_name: str) -> Dict:
        return {'q': city_name,
                'appid': os.environ.get('WEATHER_API_KEY'),
                'units': 'metric',
                'lang': 'en'}

    def _request_weather_info(self, city_name: str) -> Dict:
        params = self._get_weather_api_params(city_name=city_name)
        resp = requests.get(self.api_url, params=params)
        resp.raise_for_status()
        return resp.json()

    def _get_day_time_description(self, hour: int) -> str:
        return 'night' if hour < 6 else 'day' if 6 <= hour < 15 else 'evening-morning'

    def _get_local_timezone_hour(self, info: Dict) -> int:
        info_timezone = info.get('timezone')
        local_timezone = timezone(timedelta(seconds=info_timezone))
        local_timezone_hour = datetime.now(local_timezone).hour
        return local_timezone_hour

    def _get_weather_report(self, city: Dict, info: Dict, local_hour: int) -> Dict:
        temperature = info.get('main', {}).get('temp')
        state = info.get('weather', [])[0]['main']
        city_name = info.get('name')
        return {
            'time': self._get_day_time_description(hour=local_hour),
            'temperature_degrees': round(temperature),
            'state': state,
            'city_name': city_name.capitalize(),
            'city_id': city.get('id')
        }

    def get_weather(self, city: Dict) -> Union[Dict, None]:
        try:
            info = self._request_weather_info(city_name=city.get('name'))
            local_hour = self._get_local_timezone_hour(info=info)
            weather = self._get_weather_report(city=city, info=info, local_hour=local_hour)
            return weather
        except requests.HTTPError:
            return None

    def get_all_cities_from_repository(self) -> List[Dict]:
        all_cities = self._city_repository.query.all()
        return [city.dict() for city in all_cities]

    def register_city(self, city: CityEntity) -> None:
        city = self._city_repository(**city.dict())
        city.add_to_repository()

    def remove_city(self, _id: int) -> bool:
        city = self.get_city_by_id(_id=_id)
        if not city:
            return False

        city.remove_from_repository()
        return True

    def get_city_by_id(self, _id: int):
        return self._city_repository.query.filter_by(id=_id).first()

    def get_all_cities_current_weather(self) -> List[Dict]:
        all_cities = self.get_all_cities_from_repository()
        if all_cities:
            return [self.get_weather(city=city) for city in all_cities]
        return []
