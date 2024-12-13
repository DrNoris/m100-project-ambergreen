from ambergreen.AiManagement.footprintPredictionManagement.EmmisionsPredictor import EmissionsPredictor
from ambergreen.consumptionDataManagement.service.consumptionDataService import ConsumptionDataService
from ambergreen.institutionManagement.entity.institution import Institution
from ambergreen.institutionManagement.service.institutionService import InstitutionService
from ambergreen.providersManagement.service.providerService import ProviderService
from ambergreen.utils.EmmisionsDataLoader import EmissionsDataLoader


class EmmisionsPredictorService:
    def __init__(self, providers_service: ProviderService, consumption_data_service: ConsumptionDataService, institution_service: InstitutionService):
        self.__providers_service = providers_service
        self.__consumption_data_service = consumption_data_service
        self.__institution_service = institution_service
        self.__dict: dict[int, EmissionsPredictor] = {}

    def getPredictions(self, institution_id: int, months_ahead: int = 24, json_path=None):
        if institution_id in self.__dict:
            return self.__dict[institution_id].predict(months_ahead=months_ahead)
        else:
            return self.trainPredictor(institution_id, months_ahead, json_path)

    def trainPredictor(self, institution_id: int, months_ahead: int = 24, json_path=None):
        emission_predictor = EmissionsPredictor()
        institution = self.__institution_service.getInstitution(institution_id)
        if institution is None:
            raise RuntimeError('Institution not found')

        data = self.__consumption_data_service.getConsumptionDataForInstitution(institution_id)

        electricity_factor = self.__providers_service.getProvider(institution.getEnergyProvider()).getEmissionFactor()
        gas_factor = self.__providers_service.getProvider(institution.getGasProvider()).getEmissionFactor()
        water_factor = self.__providers_service.getProvider(institution.getWaterProvider()).getEmissionFactor()

        data_loader = EmissionsDataLoader(emission_factors={
            'electricity': electricity_factor,
            'gas': gas_factor,
            'water': water_factor
        })
        if data is None:
            if json_path is None:
                raise RuntimeError('Json path not specified')

            data_loader.load_from_json(json_path)
            emission_predictor.train(data_loader.get_emissions_data())
            self.__dict[institution_id] = emission_predictor
            return emission_predictor.predict(months_ahead=months_ahead)
        else:
            emission_predictor.train(data_loader.process_json_data(data))
            self.__dict[institution_id] = emission_predictor
            return emission_predictor.predict(months_ahead=months_ahead)