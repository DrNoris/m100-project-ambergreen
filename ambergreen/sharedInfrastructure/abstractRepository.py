from abc import ABC, abstractmethod
from typing import Generic, TypeVar

E = TypeVar("E")

class AbstractRepository(ABC, Generic[E]):

    @abstractmethod
    def add(self, entity) -> E:
        pass

    @abstractmethod
    def get(self, entity_id) -> E:
        pass

    @abstractmethod
    def remove(self, entity_id):
        pass

    @abstractmethod
    def update(self, entity) -> E:
        pass

    @abstractmethod
    def getAll(self):
        pass