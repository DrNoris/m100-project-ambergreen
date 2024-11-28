from typing import List

from consumptionDataManagement.entity.consumptionData import ConsumptionData
from consumptionDataManagement.validator.consumptionDataValidator import ConsumptionDataValidator
from sharedInfrastructure.abstractRepository import AbstractRepository


class ConsumptionDataService:
    def __init__(self, repo: AbstractRepository, validator: ConsumptionDataValidator):
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


