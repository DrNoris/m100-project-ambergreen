from ambergreen.sharedInfrastructure.entity import Entity


class ConsumptionData(Entity):

    def __init__(self, month, year, energyConsumption, gasConsumption, waterConsumption, energyProvider = None, gasProvider = None, waterProvider = None, institutionId = None):
        super().__init__(institutionId)
        self.__month = month
        self.__year = year
        self.__energyConsumption = energyConsumption
        self.__gasConsumption = gasConsumption
        self.__waterConsumption = waterConsumption
        self.__energyProvider = energyProvider
        self.__gasProvider = gasProvider
        self.__waterProvider = waterProvider

    def getInstitutionId(self):
        return self.getId()

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

    def getEnergyProvider(self):
        return self.__energyProvider

    def getGasProvider(self):
        return self.__gasProvider

    def getWaterProvider(self):
        return self.__waterProvider

    def __eq__(self, other):
        return self.getInstitutionId() == other.getInstitutionId()
