from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.mapview import MapView
from ambergreen.Domain.Buildings import Building
from ambergreen.Domain.CostumeMarker import CostumeMarker
from ambergreen.Domain.CostumePopUp import *
from abc import abstractmethod
from ambergreen.Domain.ImageButton import ImageButton
from ambergreen.GUI.appRepository import AppRepository
from ambergreen.GUI.appService import AppService
from ambergreen.GUI.loginDBRepository import LoginDBRepository
from ambergreen.GUI.loginService import LoginService
from ambergreen.consumptionDataManagement.repository.consumptionDataDBRepository import ConsumptionDataDBRepository
from ambergreen.consumptionDataManagement.service.consumptionDataService import ConsumptionDataService
from ambergreen.consumptionDataManagement.validator.consumptionDataValidator import ConsumptionDataValidator

Builder.load_file("popup_design.kv")

class LoginScreen(Screen):
    def __init__(self, loginService: LoginService,**kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.loginService = loginService

    def on_login(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        result = self.loginService.login(email, password)

        if result["success"] == False:
            print("Login failed")
        else:
            consumptionDataDBRepository = ConsumptionDataDBRepository(*getLoginData())
            consumptionDataService = ConsumptionDataService(consumptionDataDBRepository, ConsumptionDataValidator())

            appRepo = AppRepository(*getLoginData())
            appService = AppService(result["institution"], appRepo, consumptionDataService)

            self.manager.get_screen("AccountAppScreen").set_user_data(result["institution"])
            self.manager.get_screen("AccountAppScreen").set_app_service(appService)
            self.manager.current = "AccountAppScreen"

    def guest_login(self):
        self.manager.current = "guest"

class AbstractAppScreen(Screen):
    def on_enter(self):
        self.min_lat = 46.75051239498986
        self.max_lat = 46.79451493081488
        self.min_lon = 23.537636894517362
        self.max_lon = 23.654332062382636

        self.map_view = MapView(zoom=16, lat=46.769838, lon=23.5875915)
        self.min_zoom = 14  # Minimum zoom level
        self.max_zoom = 17  # Maximum zoom level
        self.add_widget(self.map_view)

        self.primarie_marker = CostumeMarker(lat=Building.Primarie.value.lat, lon=Building.Primarie.value.lon)
        self.map_view.add_widget(self.primarie_marker)
        self.primarie_marker.bind(on_release=lambda instance: self.on_marker_click(2))

        #self.casaDeCulturaAStudentilor_marker = CostumeMarker(lat=Building.CasaDeCulturaAStudentilor.value.lat, lon=Building.CasaDeCulturaAStudentilor.value.lon)
        #self.map_view.add_widget(self.casaDeCulturaAStudentilor_marker)


        #self.casaDeCulturaAStudentilor_marker.bind(on_release=lambda instance: self.on_marker_click('CasaDeCulturaAStudentilor'))
        self.map_view.bind(on_touch_move=self.on_map_move)
        self.map_view.bind(zoom=self.enforce_zoom_limits)

    @abstractmethod
    def on_marker_click(self, value):
        pass

    def get_data(self, value):
        # Simulate fetching dynamic data (this could be a web service or database query)
        descriptions = {
            'Primarie': ["Primaria Cluj-Napoca", "Calea Motilor 3, Cluj-Napoca 400001", 54325, 3000, 25600, 4500, 213],
            'CasaDeCulturaAStudentilor': ["Casa de Cultura a Studentilor", "Piata Lucian Blaga 1-3, Cluj-Napoca 400347",
                                          5432, 1500, 3200, 1340, 125]

        }
        # You can replace this with actual service calls
        return descriptions.get(value, "No description available.")

    def on_map_move(self, instance, touch):
        # Get the map's current lat/lon
        # Get the current lat/lon directly from the map_view
        lat = self.map_view.lat
        lon = self.map_view.lon
        # Check if the map is outside the allowed boundaries
        if lat < self.min_lat:
            lat = self.min_lat
        elif lat > self.max_lat:
            lat = self.max_lat

        if lon < self.min_lon:
            lon = self.min_lon
        elif lon > self.max_lon:
            lon = self.max_lon


        # Update the map to stay within the boundaries
        self.map_view.center_on(lat, lon)

    def enforce_zoom_limits(self, instance, zoom):
        """Ensure the zoom level stays within the defined limits."""
        if zoom < self.min_zoom:
            instance.zoom = self.min_zoom
        elif zoom > self.max_zoom:
            instance.zoom = self.max_zoom

class GuestAppScreen(AbstractAppScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appService = None

    def set_app_service(self, appService: AppService):
        self.appService = appService

    def on_marker_click(self, value):
        data = self.appService.getData(value)

        popup = CostumePopUpGuest(data)
        popup.open()

class AccountAppScreen(AbstractAppScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_data = None
        self.appService = None

    def set_user_data(self, user_data):
        self.user_data = user_data

    def set_app_service(self, appService: AppService):
        self.appService = appService

    def on_enter(self):
        super().on_enter()

        self.account_button = ImageButton(image_source="ambergreen/Media/account-icon.png")
        self.account_button.size = (self.width * 0.1, self.height * 0.1)
        self.account_button.pos_hint = {'x': 0.03, 'top': 0.95}

        self.account_button.bind(on_release=self.on_account_button_click)

        self.add_widget(self.account_button)

    def on_marker_click(self, value):
        data = self.appService.getData(value)

        popup = CostumePopUpAccount(data)
        popup.open()

    def on_account_button_click(self, instance):
        popup = CostumePopUpAccountMenu(self.user_data, self.appService)
        popup.open()

class Main(App):
    def build(self):
        sm = ScreenManager()

        loginRepo = LoginDBRepository(*getLoginData())
        loginService = LoginService(loginRepo)


        # Add screens to ScreenManager
        sm.add_widget(LoginScreen(loginService, name="login"))
        sm.add_widget(GuestAppScreen(name="guest"))
        sm.add_widget(AccountAppScreen(name="AccountAppScreen"))

        return sm

def getLoginData():
    return ["localhost", "m100", "postgres", "noris2580"]


if __name__ == "__main__":
    Main().run()
