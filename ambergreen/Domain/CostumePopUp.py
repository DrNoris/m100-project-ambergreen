import datetime
import os

from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

from ambergreen.AiManagement.footprintPredictionManagement.emmisionsPredictor import EmissionsPredictor
from ambergreen.AiManagement.recomandationsManagement.recomandationService import RecomandationService
from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData
from ambergreen.consumptionDataManagement.service.consumptionDataService import ConsumptionDataService
from ambergreen.footprintCalculatorManagement.footprintCalculator import FootprintCalculator
from ambergreen.institutionManagement.repository.institutionDBRepository import InstitutionDBRepository
from ambergreen.institutionManagement.service import institutionService
from ambergreen.institutionManagement.service.institutionService import InstitutionService
from ambergreen.institutionManagement.validator.institutionValidator import InstitutionValidator
from ambergreen.providersManagement.repository.providersDBRepository import ProviderDBRepository
from ambergreen.providersManagement.service.providerService import ProviderService
from ambergreen.utils.emmisionsDataLoader import EmissionsDataLoader


class CostumePopUpAccountData(Popup):
    def __init__(self, user_data, data, **kwargs):
        super().__init__(**kwargs)
        self.user_data = user_data
        self.data = data
        self.title = self.user_data['name']

    def on_open(self):
        self.ids.location.text = self.user_data['address']
        self.ids.gasNumber.text = str(self.data['gas_m3']) + ' m³'
        self.ids.waterNumber.text = str(self.data['water_m3']) + ' m³'
        self.ids.electricityNumber.text = str(self.data['energy_kwh']) + ' kWh'
        self.ids.CO2Number.text = str(self.data['co2_footprint']) + ' t'
        self.ids.treeNumber.text = str(self.data['trees_footprint'])

class CostumePopUpGuest(Popup):
    def __init__(self, user_data, data, **kwargs):
        super().__init__(**kwargs)
        self.user_data = user_data
        self.data = data
        self.title = self.user_data['name']

    def on_open(self):
        self.ids.location.text = self.user_data['address']
        self.ids.CO2Number.text = str(self.data['co2_footprint']) + ' t'
        self.ids.treeNumber.text = str(self.data['trees_footprint'])

class CostumePopUpAccountMenu(Popup):
    def __init__(self, institution, consumptionDataService: ConsumptionDataService, **kwargs):
        super().__init__(**kwargs)
        self.institution = institution
        self.ids.title_label.text = institution["name"]
        self.consumptionDataService = consumptionDataService

    def on_calculator_press(self):
        self.dismiss()
        popup = CalculatorPopup()
        popup.open()

    def on_insert_data_press(self):
        print("Insert button pressed")
        self.dismiss()
        popup = InsertDataPopup(on_result=self.handle_insert_result)
        popup.open()

    def handle_insert_result(self, energy_value, water_value, gas_value):
        try:
            self.consumptionDataService.addConsumptionData(ConsumptionData(self.institution["id"],
                datetime.datetime.now().month, datetime.datetime.now().year, float(energy_value), float(gas_value), float(water_value)))
        except Exception as e:
            print(e)
            #TODO error popup

    def on_view_data_press(self):
        data = self.consumptionDataService.getConsumptionDataForInstitution(self.institution["id"], size=6)
        popup = GraphPopup(data)
        popup.open()

    def on_prediction_press(self):
        print("Prediction button pressed")
        # Add functionality for the Prediction button here

    def on_tips_press(self):
        # start instantiere
        providerRepo = ProviderDBRepository("localhost", "m100", "postgres", "noris2580")
        providersService = ProviderService(providerRepo)

        institutionRepo = InstitutionDBRepository("localhost", "m100", "postgres", "noris2580")
        institutionValidator = InstitutionValidator()
        institutionsService = InstitutionService(institutionRepo, institutionValidator)
        # stop instantiere

        # start get predictii
        primarie = institutionsService.getInstitution(1)

        primarie_electricity_factor = providersService.getProvider(primarie.getEnergyProvider()).getEmissionFactor()
        primarie_gas_factor = providersService.getProvider(primarie.getGasProvider()).getEmissionFactor()
        primarie_water_factor = providersService.getProvider(primarie.getWaterProvider()).getEmissionFactor()

        primarie_data_loader = EmissionsDataLoader(emission_factors={
            'electricity': primarie_electricity_factor,
            'gas': primarie_gas_factor,
            'water': primarie_water_factor
        })

        primarie_predictor = EmissionsPredictor()
        primarie_data_loader.load_from_json("ambergreen/GUI/cluj_napoca_town_hall_generated_consumption_data.json")
        primarie_predictor.train(primarie_data_loader.get_emissions_data())
        predictions = primarie_predictor.predict(months_ahead=24)
        print(predictions)
        # stop get predictii

        # start recomandari
        recomandari = RecomandationService(providersService, self.consumptionDataService, institutionsService)
        rec = recomandari.getRecomandations(primarie_data_loader.get_emissions_data())

        print(rec)
        # stop recomandari


class CalculatorPopup(Popup):
    show_results = BooleanProperty(False)
    co2_footprint = NumericProperty(0)
    trees_footprint = NumericProperty(0)

    def calculate(self):
        energy_value = self.ids.electricity_id.text
        water_value = self.ids.water_id.text
        gas_value = self.ids.gas_id.text

        footprint_calculator = FootprintCalculator()

        data = {'energy_kwh': float(energy_value),
                'gas_m3': float(water_value),
                'water_m3': float(gas_value)}

        data['co2_footprint'] = footprint_calculator.calculate(data)
        data['trees_footprint'] = round(data['co2_footprint'] / 0.89, 2)

        self.co2_footprint = data['co2_footprint']
        self.trees_footprint = data['trees_footprint']

        self.show_results = True

class InsertDataPopup(Popup):
    def __init__(self, on_result, **kwargs):
        super().__init__(**kwargs)
        self.on_result = on_result

    def insert(self):
        energy_value = self.ids.electricity_id.text
        water_value = self.ids.water_id.text
        gas_value = self.ids.gas_id.text

        if self.on_result:
            self.on_result(energy_value, water_value, gas_value)

class GraphPopup(Popup):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.title = "Consumption Data"
        self.size_hint = (0.9, 0.9)

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        layout.add_widget(self.create_graph(data))

    def create_graph(self, data):
        months = [str(entry['month']) for entry in data][::-1]
        gas = [entry['gas_m3'] for entry in data][::-1]
        water = [entry['water_m3'] for entry in data][::-1]
        electricity = [entry['energy_kwh'] for entry in data][::-1]

        fig, ax = plt.subplots(figsize=(8, 6))
        x = np.arange(len(months))
        width = 0.2

        ax.bar(x - width, gas, width, label='Gas - m³', color='red')
        ax.bar(x, water, width, label='Water - m³', color='blue')
        ax.bar(x + width, electricity, width, label='Electricity - kWh', color='yellow')

        ax.set_xlabel('Months')
        ax.set_ylabel('Consumption')
        ax.set_title('Last ' + str(len(data)) + ' Months of Consumption Data')
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()

        return FigureCanvasKivyAgg(fig)