from infrastructure.adapters.orm_adapter import ORMAdapter


class PersistenceAdapter:

    def __new__(cls, *args, **kwargs):
        return ORMAdapter()


repository = PersistenceAdapter()
