from abc import abstractmethod, ABC
from typing import TypeVar, List
from ambergreen.sharedInfrastructure.abstractRepository import AbstractRepository

import psycopg2 #for PostgreSQL

E = TypeVar("E")

class AbstractPostgresRepository(AbstractRepository[E]):
    @abstractmethod
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host = host,
            database = database,
            user = user,
            password= password
        )
        self.cursor = self.connection.cursor()
        self.createTable()
        self.connection.commit()

    def get(self, entity_id: int) -> E:
        self.cursor.execute(
            "SELECT * FROM " + self.getTableName() + " WHERE id = %s",
            (entity_id,)
        )
        result = self.cursor.fetchone()

        if result is None:
            raise KeyError(f"Entity with ID {entity_id} not found.")

        return self.mapRowToEntity(result)

    def getAll(self) -> List[E]:
        self.cursor.execute(
            "SELECT * FROM " + self.getTableName()
        )
        result = self.cursor.fetchall()
        if result is None:
            return []

        return [self.mapRowToEntity(row) for row in result]


    def remove(self, entity_id: int) -> None:
        self.cursor.execute(
            "DELETE FROM " + self.getTableName() + " WHERE id = %s",
            (entity_id,)
        )
        if self.cursor.rowcount == 0:
            raise KeyError(f"Institution with ID {entity_id} does not exist.")

        self.connection.commit()



    @abstractmethod
    def createTable(self):
        pass

    @abstractmethod
    def getTableName(self) -> str:
        pass

    @abstractmethod
    def mapRowToEntity(self, row) -> E:
        pass