from abc import ABC, abstractmethod


class AppConfigurationService(ABC):

    @abstractmethod
    def app(self):
        ...

    @abstractmethod
    def add_configurations(self) -> None:
        ...
