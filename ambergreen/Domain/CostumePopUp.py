from kivy.uix.popup import Popup

from ambergreen.GUI.appService import AppService


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
    def __init__(self, institution, appService: AppService, **kwargs):
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
        # Add functionality for this button here

    def on_prediction_press(self):
        print("Prediction button pressed")
        # Add functionality for the Prediction button here

    def on_tips_press(self):
        print("Tips button pressed")
        # Add functionality for the Tips button here

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