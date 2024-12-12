from typing import Dict, List
from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.consumptionDataManagement.validator.consumptionDataValidator import ConsumptionDataValidator
from ambergreen.sharedInfrastructure.abstractRepository import AbstractRepository


class InMemoryRepository(AbstractRepository[ConsumptionData]):
    def __init__(self):
        self._store: Dict[str, ConsumptionData] = {}
        self._id_counter = 1

    def add(self, consumptionData: ConsumptionData) -> ConsumptionData:
        key = f"{consumptionData.getInstitutionId()}_{consumptionData.getMonth()}_{consumptionData.getYear()}"
        self._store[key] = consumptionData
        return consumptionData

    def remove(self, key: List[int]) -> None:
        composite_key = f"{key[0]}_{key[1]}_{key[2]}"
        if composite_key not in self._store:
            raise KeyError(f"ConsumptionData with key {composite_key} does not exist.")
        del self._store[composite_key]

    def get(self, key: List[int]) -> ConsumptionData:
        composite_key = f"{key[0]}_{key[1]}_{key[2]}"
        if composite_key not in self._store:
            raise KeyError(f"ConsumptionData with key {composite_key} does not exist.")
        return self._store[composite_key]

    def update(self, consumptionData: ConsumptionData) -> ConsumptionData:
        key = f"{consumptionData.getInstitutionId()}_{consumptionData.getMonth()}_{consumptionData.getYear()}"
        if key not in self._store:
            raise KeyError(f"ConsumptionData with key {key} does not exist.")
        self._store[key] = consumptionData
        return consumptionData

    def getAll(self) -> List[ConsumptionData]:
        return list(self._store.values())


import unittest
from ambergreen.consumptionDataManagement.service.consumptionDataService import ConsumptionDataService


class TestConsumptionDataService(unittest.TestCase):
    def setUp(self):
        # Set up the repository, validator, and service
        self.repo = InMemoryRepository()
        self.validator = ConsumptionDataValidator()
        self.service = ConsumptionDataService(self.repo, self.validator)

        # Sample data
        self.sample_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )

    def test_add_consumption_data(self):
        self.service.addConsumptionData(self.sample_data)
        all_data = self.service.getAllConsumptionData()
        self.assertEqual(len(all_data), 1)
        self.assertEqual(all_data[0].getInstitutionId(), 1)

    def test_remove_consumption_data(self):
        self.service.addConsumptionData(self.sample_data)
        self.service.removeConsumptionData([1, 5, 2023])
        all_data = self.service.getAllConsumptionData()
        self.assertEqual(len(all_data), 0)

    def test_update_consumption_data(self):
        self.service.addConsumptionData(self.sample_data)
        updated_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=200.0,
            gasConsumption=90.0,
            waterConsumption=60.0,
            institutionId=1
        )
        self.service.updateConsumptionData(updated_data)
        fetched_data = self.service.getConsumptionData(1, 5, 2023)
        self.assertEqual(fetched_data.getEnergyConsumption(), 200.0)

    def test_get_consumption_data(self):
        self.service.addConsumptionData(self.sample_data)
        data = self.service.getConsumptionData(1, 5, 2023)
        self.assertEqual(data.getInstitutionId(), 1)
        self.assertEqual(data.getMonth(), 5)
        self.assertEqual(data.getYear(), 2023)

    def test_get_all_consumption_data(self):
        data1 = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        data2 = ConsumptionData(
            month=6,
            year=2023,
            energyConsumption=170.0,
            gasConsumption=85.0,
            waterConsumption=55.0,
            institutionId=1
        )
        self.service.addConsumptionData(data1)
        self.service.addConsumptionData(data2)

        all_data = self.service.getAllConsumptionData()
        self.assertEqual(len(all_data), 2)
        self.assertEqual(all_data[0].getMonth(), 5)
        self.assertEqual(all_data[1].getMonth(), 6)


if __name__ == "__main__":
    unittest.main()
