from abc import ABC, abstractmethod

class RepositoryService(ABC):

    @abstractmethod
    def db(self):
        ...
