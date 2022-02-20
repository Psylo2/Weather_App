from typing import Dict, List, Union

from infrastructure.ports.city_repository_port import CityRepository
from infrastructure.queries.services import CityRepositoryQueryService

class CityRepositoryQuery(CityRepositoryQueryService):
    def __init__(self):
        pass

    def add_city(self, city_data: Dict) -> CityRepository:
        city = CityRepository(**city_data)
        city.add_to_repository()
        return city

    def remove_city(self, city: CityRepository) -> None:
        city.remove_from_repository()

    def get_all_cities(self) -> List[Dict]:
        all_cities = CityRepository.query.all()
        return [city.dict() for city in all_cities]

    def get_city_by_id(self, id: int) -> Union[CityRepository, None]:
        return CityRepository.query.filter_by(id=id).first()

    def get_all_cities_name_list(self) -> List[str]:
        all_cities_tuples = CityRepository.query.with_entities(CityRepository.name).all()
        return list(map(lambda x: x[0], all_cities_tuples))
