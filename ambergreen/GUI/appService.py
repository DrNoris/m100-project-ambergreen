from ambergreen.GUI.appRepository import AppRepository
from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.consumptionDataManagement.service.consumptionDataService import ConsumptionDataService
import datetime

class AppService:
    def __init__(self, institution, appRepo: AppRepository, consumptionDataService: ConsumptionDataService):
        self.appRepo = appRepo
        self.institution = institution
        self.consumptionDataService = consumptionDataService

    def addConsumptionData(self, value1, value2, value3):
        consumptionData = ConsumptionData(self.institution["id"], datetime.datetime.now().month,
                        datetime.datetime.now().year, float(value1), float(value2), float(value3))
        self.consumptionDataService.addConsumptionData(consumptionData)

    def getData(self, id):
            return self.appRepo.getData(id)

