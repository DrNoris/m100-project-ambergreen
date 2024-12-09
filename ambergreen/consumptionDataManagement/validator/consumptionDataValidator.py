from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.sharedInfrastructure.validator import Validator


class ConsumptionDataValidator(Validator):
    def __init__(self):
        pass

    def validate(self, consumptionData):
        if not isinstance(consumptionData, ConsumptionData):
            raise TypeError(f"Expected ConsumptionData, got {type(consumptionData).__name__}.")

        if not consumptionData.getInstitutionId() or not isinstance(consumptionData.getInstitutionId(), int) or consumptionData.getInstitutionId() < 0:
            raise ValueError("Id must be positive integer.")

        if not consumptionData.getWaterConsumption() or not isinstance(consumptionData.getWaterConsumption(), float) or consumptionData.getWaterConsumption() < 0:
            raise ValueError("Water consumption cannot be lower than 0 and must be a valid Float.")

        if not consumptionData.getGasConsumption() or not isinstance(consumptionData.getGasConsumption(), float) or consumptionData.getGasConsumption() < 0:
            raise ValueError("Gas consumption cannot be lower than 0 and must be a valid Float.")

        if not consumptionData.getEnergyConsumption() or not isinstance(consumptionData.getEnergyConsumption(), float) or consumptionData.getEnergyConsumption() < 0:
            raise ValueError("Energy consumption cannot be lower than 0 and must be a valid Float.")

        if not consumptionData.getYear() or not isinstance(consumptionData.getYear(), int) or consumptionData.getYear() < 1900:
            raise ValueError("Year cannot be lower than 0 and must be a valid Integer (higher than 1900).")

        if not consumptionData.getMonth() or not isinstance(consumptionData.getMonth(), int) or consumptionData.getMonth() <= 0 or consumptionData.getMonth() > 12:
            raise ValueError("Water cannot be lower than 0 and must be a valid Integer.")

        return True