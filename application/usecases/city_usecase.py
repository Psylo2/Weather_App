import os
from flask import flash
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Union

from infrastructure.queries.services import CityRepositoryQueryService
from application.usecases.services import CityUseCaseService
from domain.entities import CityEntity


class CityUseCase(CityUseCaseService):

    def __init__(self, city_repository_queries_service: CityRepositoryQueryService):
        self.city_repository_queries_service = city_repository_queries_service

    @property
    def api_url(self) -> str:
        return 'https://api.openweathermap.org/data/2.5/weather'

    def register_city(self, city_name: str) -> None:
        city = CityEntity(name=city_name)
        city_info = self._request_weather_info(city_name=city.name)
        global_city_name = city_info.get('name')

        if not global_city_name:
            flash("The city doesn't exist!")
            return None

        is_city_in_repository = global_city_name in self.city_repository_queries_service.get_all_cities_name_list()
        if is_city_in_repository:
            flash("The city has already been added to the list!")
            return None

        city.name = global_city_name
        self.city_repository_queries_service.add_city(city.dict())

    def remove_city(self, _id: int) -> None:
        city = self.city_repository_queries_service.get_city_by_id(id=_id)
        if not city:
            flash("City ID not exists")
            return None

        self.city_repository_queries_service.remove_city(city=city)
        flash("City has removed")

    def get_all_cities_current_weather(self) -> List[Dict]:
        all_cities = self.get_all_cities_from_repository()

        if not all_cities:
            flash("Please Add a City!")
            return []

        return [self.get_weather(city=city) for city in all_cities]

    def _get_weather_api_params(self, city_name: str) -> Dict:
        return {'q': city_name,
                'appid': os.environ.get('WEATHER_API_KEY'),
                'units': 'metric',
                'lang': 'en'}

    def _request_weather_info(self, city_name: str) -> Dict:
        params = self._get_weather_api_params(city_name=city_name)
        resp = requests.get(self.api_url, params=params)
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
        return self.city_repository_queries_service.get_all_cities()
