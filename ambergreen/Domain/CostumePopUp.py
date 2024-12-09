from kivy.uix.popup import Popup

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
        self.ids.CO2Number.text = str(self.dynamic_data[5])
        self.ids.treeNumber.text = str(self.dynamic_data[6])


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
    def __init__(self, dynamic_data = None, **kwargs):
        super().__init__(**kwargs)
        self.dynamic_data = dynamic_data
        self.ids.title_label.text = self.dynamic_data

    def on_calculator_press(self):
        print("Calculator button pressed")
        self.dismiss()
        popup = CalculatorPopup()
        popup.open()

    def on_insert_data_press(self):
        print("Insert button pressed")
        self.dismiss()
        popup = InsertDataPopup()
        popup.open()

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
    def calculate(self):
        value1 = self.ids.electricity_id.text
        value2 = self.ids.water_id.text
        value3 = self.ids.gas_id.text
        print(f"Calculating with values: {value1}, {value2}, {value3}")

class InsertDataPopup(Popup):
    def insert(self):
        value1 = self.ids.electricity_id.text
        value2 = self.ids.water_id.text
        value3 = self.ids.gas_id.text
        print(f"Inserting data values: {value1}, {value2}, {value3}")