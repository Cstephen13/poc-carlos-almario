from abc import ABC, abstractmethod


class FilterManager(ABC):

    @abstractmethod
    def filter(self, kwargs: dict):
        pass


class CreateManager(ABC):

    @abstractmethod
    def create(self, data: dict):
        pass


class UpdateManager(ABC):

    @abstractmethod
    def update(self, data: dict):
        pass
