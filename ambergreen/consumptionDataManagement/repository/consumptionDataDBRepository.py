from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.sharedInfrastructure.abstractPostgresRepository import AbstractPostgresRepository


class ConsumptionDataDBRepository(AbstractPostgresRepository[ConsumptionData]):
    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)

    def add(self, consumptionData: ConsumptionData):
        self.cursor.execute(
            f"INSERT INTO {self.getTableName()} "
            f"(institution_id, month, year, energy_consumption, water_consumption, gas_consumption, energy_provider, water_provider, gas_provider) "
            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                consumptionData.getId(),
                consumptionData.getMonth(),
                consumptionData.getYear(),
                consumptionData.getEnergyConsumption(),
                consumptionData.getWaterConsumption(),
                consumptionData.getGasConsumption(),
                consumptionData.getEnergyProvider() if consumptionData.getEnergyProvider() is not None else None,
                consumptionData.getWaterProvider() if consumptionData.getWaterProvider() is not None else None,
                consumptionData.getGasProvider() if consumptionData.getGasProvider() is not None else None
            )
        )
        self.connection.commit()

    def update(self, consumptionData: ConsumptionData):
        self.cursor.execute(
            f"UPDATE {self.getTableName()}, SET energy_consumption = %s, water_consumption = %s, gas_consumption = %s,WHERE institution_id = %s, year = %s, month = %s",
            (consumptionData.getEnergyConsumption(), consumptionData.getWaterConsumption(), consumptionData.getGasConsumption(), consumptionData.getInstitutionId(), consumptionData.getYear(), consumptionData.getMonth())
        )
        self.connection.commit()

    def createTable(self):
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS consumption_data (
                                        instiution_id INT PRIMARY KEY,
                                        month int NOT NULL,
                                        year int NOT NULL,
                                        constraint fk_institution FOREIGN KEY (instiution_id) REFERENCES Institutions(id) ON DELETE CASCADE,
                                        energy_consumption TEXT NOT NULL,
                                        water_consumption TEXT NOT NULL,
                                        gas_consumption TEXT NOT NULL,
                                        energy_provider TEXT,
                                        water_provider TEXT,
                                        gas_provider TEXT
                                    )        
                        """)
        self.connection.commit()

    def getTableName(self) -> str:
        return "consumption_data"

    def mapRowToEntity(self, row) -> ConsumptionData:
        institutionId = int(row[0])
        month = row[1]
        year = row[2]
        energy_consumption = row[3]
        water_consumption = row[4]
        gas_consumption = row[5]
        energy_provider = None
        water_provider = None
        gas_provider = None
        if row[6] is not None:
            energy_provider = row[6]
        if row[7] is not None:
            water_provider = row[7]
        if row[8] is not None:
            gas_provider = row[8]
        return ConsumptionData(month, year, energy_consumption, water_consumption, gas_consumption, energy_provider, water_provider, gas_provider, institutionId)

    def get(self, entity_id) -> ConsumptionData | None:
        if isinstance(entity_id, list):
            self.cursor.execute(
                "SELECT * FROM " + self.getTableName() + " WHERE institution_id = %s, month = %s, year = %s",
                (entity_id[0], entity_id[1], entity_id[2])
            )
            result = self.cursor.fetchone()

            if result is None:
                raise KeyError(f"Entity with institution ID {entity_id[0]}, on month {entity_id[1]} and year {entity_id[2]} not found.")

            return self.mapRowToEntity(result)

    def remove(self, entity_id) -> None:
        if isinstance(entity_id, list):
            self.cursor.execute(
                "DELETE * FROM " + self.getTableName() + " WHERE institution_id = %s, month = %s, year = %s",
                (entity_id[0], entity_id[1], entity_id[2])
            )
            if self.cursor.rowcount == 0:
                raise KeyError(f"Entity with institution ID {entity_id[0]}, on month {entity_id[1]} and year {entity_id[2]} not found.")

            self.connection.commit()
