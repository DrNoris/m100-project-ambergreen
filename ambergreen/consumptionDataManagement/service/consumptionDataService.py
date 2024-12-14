from typing import List, Dict

from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.consumptionDataManagement.repository.consumptionDataDBRepository import ConsumptionDataDBRepository
from ambergreen.consumptionDataManagement.validator.consumptionDataValidator import ConsumptionDataValidator
from ambergreen.dto.ConsumptionDataFilterDTO import ConsumptionDataFilterDTO
from ambergreen.sharedInfrastructure.abstractRepository import AbstractRepository
from ambergreen.utils.emmisionsDataLoader import EmissionsDataLoader


class ConsumptionDataService:
    def __init__(self, repo: ConsumptionDataDBRepository, validator: ConsumptionDataValidator):
        self.repo = repo
        self.validator = validator

    def addConsumptionData(self, consumptionData: ConsumptionData):
        """
        Add consumption data to the repository.
        Raises RuntimeError if validation or repository operation fails.
        """
        try:
            self.validator.validate(consumptionData)
            self.repo.add(consumptionData)
        except Exception as e:
            raise RuntimeError(f"Failed to add consumption data: {e}")

    def removeConsumptionData(self, consumptionData: ConsumptionData):
        """
        Remove consumption data from the repository.
        Raises RuntimeError if the repository operation fails.
        """
        try:
            self.repo.remove(consumptionData)
        except Exception as e:
            raise RuntimeError(f"Failed to remove consumption data: {e}")

    def updateConsumptionData(self, consumptionData: ConsumptionData):
        """
        Update consumption data in the repository.
        Raises RuntimeError if validation or repository operation fails.
        """
        try:
            self.validator.validate(consumptionData)
            self.repo.update(consumptionData)
        except Exception as e:
            raise RuntimeError(f"Failed to update consumption data: {e}")

    def getConsumptionData(self, institution_id: int, month: int, year: int):
        """
        Retrieve consumption data by institution ID, month, and year.
        Raises RuntimeError if the repository operation fails.
        """
        try:
            entity_key = [institution_id, month, year]
            return self.repo.get(entity_key)
        except Exception as e:
            raise RuntimeError(
                f"Failed to retrieve consumption data for Institution ID {institution_id}, Month {month}, Year {year}: {e}"
            )

    def getAllConsumptionData(self) -> List[ConsumptionData]:
        return self.repo.getAll()

    def getConsumptionDataForInstitution(self, institution_id: int, size = -1) -> List[Dict]:
        return self.repo.getConsumptionDataFiltered(ConsumptionDataFilterDTO(institution_id), size)

    def getTotalConsumptionDataForInstitution(self, institution_id: int) -> Dict:
        return self.repo.getTotalConsumptionDataFiltered(ConsumptionDataFilterDTO(institution_id))

    def saveConsumptionDataJSON(self, institution_id, json_path: str):
        data = EmissionsDataLoader.process_json_path(json_path)
        for consumption in data:
            date = consumption['month']
            year, month = map(int, date.split('-'))
            energy = consumption['energy_kwh']
            gas = consumption['gas_m3']
            water = consumption['water_m3']
            consumptionData = ConsumptionData(institution_id, month, year, energy, gas, water)
            self.repo.add(consumptionData)


