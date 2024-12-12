from ambergreen.GUI.appService import AccountAppService
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
import numpy as np

class CostumePopUpAccount(Popup):
    def __init__(self, dynamic_data, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_data = dynamic_data
        self.title = self.dynamic_data[0]

    def on_open(self):
        self.ids.location.text = self.dynamic_data[1]
        self.ids.gasNumber.text = str(self.dynamic_data[2])
        self.ids.waterNumber.text = str(self.dynamic_data[3])
        self.ids.electricityNumber.text = str(self.dynamic_data[4])
        # self.ids.CO2Number.text = str(self.dynamic_data[5])
        # self.ids.treeNumber.text = str(self.dynamic_data[6])

class CostumePopUpGuest(Popup):
    def __init__(self, dynamic_data, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_data = dynamic_data
        self.title = self.dynamic_data[0]

    def on_open(self):
        self.ids.location.text = self.dynamic_data[1]
        self.ids.CO2Number.text = str(self.dynamic_data[5])
        self.ids.treeNumber.text = str(self.dynamic_data[6])

class CostumePopUpAccountMenu(Popup):
    def __init__(self, institution, appService: AccountAppService, **kwargs):
        super().__init__(**kwargs)
        self.institution = institution
        self.ids.title_label.text = institution["name"]
        self.appService = appService

    def on_calculator_press(self):
        self.dismiss()
        popup = CalculatorPopup(on_result=self.handle_calculation_result)
        popup.open()
        #TO DO HANDLER

    def on_insert_data_press(self):
        print("Insert button pressed")
        self.dismiss()
        popup = InsertDataPopup(on_result=self.handle_insert_result)
        popup.open()

    def handle_insert_result(self, value1, value2, value3):
        self.appService.addConsumptionData(value1, value2, value3)

    def on_view_data_press(self):
        print("View data button pressed")
        data = self.appService.getDataGraph(self.institution)
        popup = GraphPopup(data)
        popup.open()

    def on_prediction_press(self):
        print("Prediction button pressed")
        # Add functionality for the Prediction button here

    def on_tips_press(self):
        print("Tips button pressed")
        self.dismiss()
        popup = InsertDataPopup(on_result=self.handle_insert_result)
        popup.open()

class CalculatorPopup(Popup):
    def __init__(self, on_result, **kwargs):
        super().__init__(**kwargs)
        self.on_result = on_result

    def calculate(self):
        value1 = self.ids.electricity_id.text
        value2 = self.ids.water_id.text
        value3 = self.ids.gas_id.text

        if self.on_result:
            self.on_result(value1, value2, value3)

class InsertDataPopup(Popup):
    def __init__(self, on_result, **kwargs):
        super().__init__(**kwargs)
        self.on_result = on_result

    def insert(self):
        value1 = self.ids.electricity_id.text
        value2 = self.ids.water_id.text
        value3 = self.ids.gas_id.text

        if self.on_result:
            self.on_result(value1, value2, value3)

class GraphPopup(Popup):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.title = "Consumption Data"
        self.size_hint = (0.9, 0.9)

        layout = BoxLayout(orientation='vertical')
        self.content = layout

        layout.add_widget(self.create_graph(data))

    def create_graph(self, data):
        months = [str(entry['month']) + '/' + str(entry['year']) for entry in data][::-1]
        gas = [entry['total_gas_consumption'] for entry in data][::-1]
        water = [entry['total_water_consumption'] for entry in data][::-1]
        electricity = [entry['total_energy_consumption'] for entry in data][::-1]

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