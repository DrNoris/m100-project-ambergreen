from enum import Enum
from collections import namedtuple

Coordinates = namedtuple('Coordinates', ['lat', 'lon', 'name'])

class Building(Enum):
    Primarie = Coordinates(lat=46.768379365378586, lon=23.5847886303172, name='Primarie')
    CasaDeCulturaAStudentilor = Coordinates(lat=46.76694741061791, lon=23.58638833455767, name='CasaDeCulturaAStudentilor')
