from ollama import chat

from ambergreen.consumptionDataManagement.service.consumptionDataService import ConsumptionDataService
from ambergreen.institutionManagement.service.institutionService import InstitutionService
from ambergreen.providersManagement.service.providerService import ProviderService
from ambergreen.utils.emmisionsDataLoader import EmissionsDataLoader


class RecomandationService:
    def __init__(self, providers_service: ProviderService, consumption_data_service: ConsumptionDataService, institution_service: InstitutionService):
        self.__consumption_data_service = consumption_data_service
        self.__institution_service = institution_service
        self.__providers_service = providers_service

    def getRecomandationsForInstitution(self, institution_id: int, json_path= None):
        institution = self.__institution_service.getInstitution(institution_id)

        electricity_factor = self.__providers_service.getProvider(institution.getEnergyProvider()).getEmissionFactor()
        gas_factor = self.__providers_service.getProvider(institution.getGasProvider()).getEmissionFactor()
        water_factor = self.__providers_service.getProvider(institution.getWaterProvider()).getEmissionFactor()

        data_loader = EmissionsDataLoader(emission_factors={
            'electricity': electricity_factor,
            'gas': gas_factor,
            'water': water_factor
        })
        data = self.__consumption_data_service.getConsumptionDataForInstitution(institution_id)
        if data is None:
            if json_path is not None:
                data_loader.load_from_json(json_path)
                return data_loader.get_emissions_data()
            else:
                raise RuntimeError("JSON Path not specified")
        else:
            return self.getRecomandations(data_loader.process_json_data(data))

    def getRecomandations(self, data):
        response = chat(
            model='llama3.2',
            messages=[
                {
                    'role': 'user',
                    'content': f"{data['month']}: {data['co2_emissions']}."
                               f"Based on this data, identify the categories where the building can improve."
                               f"For each category, suggest actionable steps the building managers can take to reduce its environmental impact, and estimate the potential percentage reduction achievable for each action."
                               f"I want you to format the reponse in this way:"
                               f"Recomandations for energy: "
                               f"..."
                               f"Recomandations for gas: "
                               f"..."
                               f"Recomandations for water: "
                               f"..."
                               f"I dont want you to use any characters like '*', '#'"
                               f"Please provide your suggestions, and begin each one with a - character."
                               f"I dont want you to write anything else after the recomandations such as 'Please note ...'"
                               f"I dont want you to write recomandations for anything else just these 3 categories (energy, gas, water)"
                }
            ],
            options={"stream": False,
                     "temperature": 0}
        )
        return response['message']['content']