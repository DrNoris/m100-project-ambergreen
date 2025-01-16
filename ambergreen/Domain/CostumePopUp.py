import datetime
import json
import os

from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

from ambergreen.AiManagement.footprintPredictionManagement.emmisionsPredictor import EmissionsPredictor
from ambergreen.AiManagement.footprintPredictionManagement.emmisionsPredictorService import EmmisionsPredictorService
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
                datetime.datetime.now().month, datetime.datetime.now().year, float(energy_value), float(water_value), float(gas_value)))
        except Exception as e:
            self.show_error_popup(e)


    def on_view_data_press(self):
        data = self.consumptionDataService.getConsumptionDataForInstitution(self.institution["id"], size=6)
        popup = GraphPopup(data)
        popup.open()

    def on_prediction_press(self):
        loading_popup = LoadingPopup()
        loading_popup.open()

        def fetch_prediction():
            try:
                providerRepo = ProviderDBRepository("localhost", "m100", "postgres", "noris2580")
                providersService = ProviderService(providerRepo)

                institutionRepo = InstitutionDBRepository("localhost", "m100", "postgres", "noris2580")
                institutionValidator = InstitutionValidator()
                institutionsService = InstitutionService(institutionRepo, institutionValidator)

                emissionsPredictorService = EmmisionsPredictorService(providersService, self.consumptionDataService,
                                                                      institutionsService)


                predictions = emissionsPredictorService.getPredictions(self.institution["id"], json_path='ambergreen/GUI/cluj_napoca_town_hall_generated_consumption_data.json')
                Clock.schedule_once(lambda dt: self.show_predictions_popup(predictions), 0)
            except Exception as e:
                error_message = str(e)
                Clock.schedule_once(lambda dt: self.show_error_popup(error_message), 0)
            finally:
                Clock.schedule_once(lambda dt: loading_popup.dismiss(), 0)

        import threading
        threading.Thread(target=fetch_prediction).start()

    def show_predictions_popup(self, predictions):
        dates = predictions["date"].tolist()
        predicted_co2 = predictions["predicted_co2"].tolist()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, predicted_co2, marker='o', linestyle='-', color='blue', label='Predicted CO2')
        ax.set_title("Predicted CO2 Emissions Over Time", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Predicted CO2", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()

        # Rotate date labels for better visibility
        plt.xticks(rotation=45, ha='right')

        # Add the matplotlib figure to the Kivy layout
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        graph_widget = FigureCanvasKivyAgg(fig)
        content.add_widget(graph_widget)

        # Add a close button
        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_press=lambda instance: pred_popup.dismiss())
        content.add_widget(close_button)

        # Create and open the popup
        pred_popup = Popup(
            title="Predictions Graph",
            content=content,
            size_hint=(0.9, 0.9),
            title_align="center",  # Centered title
            separator_color=(0.1, 0.2, 0.3, 0.5),  # Subtle separator line
            background_color=(0.1, 0.2, 0.3, 0.5),  # Semi-transparent dark background
        )

        pred_popup.open()

    def on_tips_press(self):
        # Show loading popup
        loading_popup = LoadingPopup()
        loading_popup.open()

        def fetch_recommendations():
            try:
                # Instantiate services
                providerRepo = ProviderDBRepository("localhost", "m100", "postgres", "noris2580")
                providersService = ProviderService(providerRepo)

                institutionRepo = InstitutionDBRepository("localhost", "m100", "postgres", "noris2580")
                institutionValidator = InstitutionValidator()
                institutionsService = InstitutionService(institutionRepo, institutionValidator)

                # Fetch recommendations
                recomandationService = RecomandationService(providersService, self.consumptionDataService,
                                                            institutionsService)
                rec = recomandationService.getRecomandationsForInstitution(self.institution["id"])

                # Show recommendations in a popup
                Clock.schedule_once(lambda dt: self.show_recommendations_popup(rec), 0)
            except Exception as e:
                error_message = str(e)
                # Schedule error popup on the main thread
                Clock.schedule_once(lambda dt: self.show_error_popup(error_message), 0)
            finally:
                # Schedule closing the loading popup on the main thread
                Clock.schedule_once(lambda dt: loading_popup.dismiss(), 0)

        # Run fetching in a separate thread to avoid blocking UI
        import threading
        threading.Thread(target=fetch_recommendations).start()

    def show_recommendations_popup(self, recommendations):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)

        label = Label(
            text=recommendations,
            halign='left',
            valign='top',
            size_hint_x=None,  # Let the width be set explicitly
            size_hint_y=None  # Allow the height to adjust automatically
        )
        label.bind(
            width=lambda instance, value: instance.setter('text_size')(instance, (value, None))
        )

        # Add the label to a scroll view
        scroll_view = ScrollView(size_hint=(1, 0.9), bar_width=10)
        scroll_view.add_widget(label)

        # Dynamically adjust the label's width to match the ScrollView
        def adjust_label_width(*args):
            label.width = scroll_view.width - 20  # Adjust for padding/margins

        scroll_view.bind(width=adjust_label_width)
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        # Add the scroll view and a close button to the content
        content.add_widget(scroll_view)
        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_press=lambda instance: rec_popup.dismiss())
        content.add_widget(close_button)

        # Display the popup
        rec_popup = Popup(
            title="Energy, Gas, and Water Recommendations",
            content=content,
            size_hint=(0.8, 0.8),
        )
        rec_popup.open()

    def show_error_popup(self, error_message):
        # Create and show a popup for errors
        error_popup = Popup(
            title="Error",
            content=Label(text=error_message),
            size_hint=(0.6, 0.4),
        )
        error_popup.open()


class LoadingPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Loading..."
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Animated GIF as a spinner
        spinner = Image(source="ambergreen/Media/loading-waiting.gif", anim_delay=0.05, size_hint=(1, 1))
        layout.add_widget(spinner)

        self.content = layout
        self.size_hint = (0.4, 0.4)

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
                'gas_m3': float(gas_value),
                'water_m3': float(water_value)}

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