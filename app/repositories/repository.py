from abc import abstractmethod

from pydantic import BaseModel


class Repository:

    @abstractmethod
    def save(self, entity: BaseModel):
        pass

    @abstractmethod
    def find_by_id(self, id: str):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def delete(self, id: str):
        pass