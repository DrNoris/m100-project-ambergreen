from kivy_garden.mapview import MapMarkerPopup

class CostumeMarker(MapMarkerPopup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "ambergreen/Media/green-pin-point.png"
        self.size = (100, 100)  # Set marker size