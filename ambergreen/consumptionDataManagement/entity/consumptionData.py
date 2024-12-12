from ambergreen.sharedInfrastructure.entity import Entity


class ConsumptionData(Entity):

    def __init__(self, institutionId, month, year, energyConsumption, gasConsumption, waterConsumption):
        super().__init__(institutionId)
        self.__month = month
        self.__year = year
        self.__energyConsumption = energyConsumption
        self.__gasConsumption = gasConsumption
        self.__waterConsumption = waterConsumption

    def getInstitutionId(self):
        return super().getId()

    def getMonth(self):
        return self.__month

    def getYear(self):
        return self.__year

    def getEnergyConsumption(self):
        return self.__energyConsumption

    def getGasConsumption(self):
        return self.__gasConsumption

    def getWaterConsumption(self):
        return self.__waterConsumption

    def __eq__(self, other):
        return self.getInstitutionId() == other.getInstitutionId()

    def __str__(self):
        return (
            f"ConsumptionData(InstitutionId={self.getInstitutionId()}, Month={self.__month}, Year={self.__year}, "
            f"EnergyConsumption={self.__energyConsumption}, GasConsumption={self.__gasConsumption}, "
            f"WaterConsumption={self.__waterConsumption})"
        )
