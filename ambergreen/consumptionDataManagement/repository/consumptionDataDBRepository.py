from typing import List, Dict

from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.dto.ConsumptionDataFilterDTO import ConsumptionDataFilterDTO
from ambergreen.sharedInfrastructure.abstractPostgresRepository import AbstractPostgresRepository

class ConsumptionDataDBRepository(AbstractPostgresRepository[ConsumptionData]):
    def __init__(self, host, database, user, password):
        super().__init__(host, database, user, password)

    def add(self, consumptionData: ConsumptionData):
        self.cursor.execute(
            f"INSERT INTO {self.getTableName()} "
            f"(institution_id, month, year, energy_consumption, water_consumption, gas_consumption) "
            f"VALUES (%s, %s, %s, %s, %s, %s)",
            (
                consumptionData.getInstitutionId(),
                consumptionData.getMonth(),
                consumptionData.getYear(),
                consumptionData.getEnergyConsumption(),
                consumptionData.getWaterConsumption(),
                consumptionData.getGasConsumption()
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
                                        institution_id INT,
                                        month int NOT NULL,
                                        year int NOT NULL,
                                        constraint fk_institution FOREIGN KEY (institution_id) REFERENCES Institutions(id) ON DELETE CASCADE,
                                        energy_consumption FLOAT NOT NULL,
                                        water_consumption FLOAT NOT NULL,
                                        gas_consumption FLOAT NOT NULL,
                                        energy_provider TEXT,
                                        water_provider TEXT,
                                        gas_provider TEXT,
                                        PRIMARY KEY (institution_id, month, year)
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
        return ConsumptionData(institutionId, month, year, energy_consumption, water_consumption, gas_consumption)

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

    def getConsumptionDataFiltered(self, consumptionDataFilterDTO: ConsumptionDataFilterDTO, size) -> List[Dict]:
        sql = "SELECT * FROM " + self.getTableName() + " "

        values = []

        if consumptionDataFilterDTO is not None:
            sql = sql + "WHERE institution_id = %s"
            values.append(consumptionDataFilterDTO.get_institution_id())

        sql = sql + " ORDER BY year DESC, month DESC"

        if size != -1:
            sql = sql + " LIMIT %s"
            values.append(size)

        self.cursor.execute(sql, values)
        results = self.cursor.fetchall()

        list = []
        for result in results:
            consumptionData = self.mapRowToEntity(result)
            list.append(
                {
                    "month": str(consumptionData.getYear()) + "-" + str(consumptionData.getMonth()),
                    "energy_kwh": float(consumptionData.getEnergyConsumption()),
                    "gas_m3": float(consumptionData.getGasConsumption()),
                    "water_m3": float(consumptionData.getWaterConsumption()),
                }
            )

        return list

    def getTotalConsumptionDataFiltered(self, consumptionDataFilterDTO: ConsumptionDataFilterDTO) -> Dict:
        sql = "SELECT * FROM " + self.getTableName() + " "

        values = []
        if consumptionDataFilterDTO is not None:
            sql = sql + "WHERE institution_id = %s"
            values.append(consumptionDataFilterDTO.get_institution_id())

        self.cursor.execute(sql, values)
        results = self.cursor.fetchall()

        total_energy = 0.0
        total_gas = 0.0
        total_water = 0.0

        for result in results:
            consumptionData = self.mapRowToEntity(result)
            total_energy += float(consumptionData.getEnergyConsumption())
            total_gas += float(consumptionData.getGasConsumption())
            total_water += float(consumptionData.getWaterConsumption())

        return {
            "energy_kwh": round(total_energy, 2),
            "gas_m3": round(total_gas, 2),
            "water_m3": round(total_water, 2),
        }