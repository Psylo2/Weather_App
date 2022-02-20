from infrastructure.queries import CityRepositoryQuery
from application_core.services import FactoryService


class Factory(FactoryService):
    def __init__(self):
        self._query_city_repository = None

    def query_city_repository(self) -> CityRepositoryQuery:
        if not self._query_city_repository:
            self._query_city_repository = CityRepositoryQuery()
        return self._query_city_repository
