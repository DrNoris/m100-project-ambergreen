class FootprintCalculator:
    def __init__(self, emission_factors = {
        'energy_kwh': 0.482,
        'gas_m3': 1.9,
        'water_m3': 10.6
    }):
        """"
        Initialize with a dictionary of emission factors.
        Example:
        {
            'energy': 0.5,
            'gas': 2.1,
            'water': 0.3
        }
        """
        self.__emission_factors = emission_factors


    def setEmmisionFactors(self, emission_factors):
        self.__emission_factors = emission_factors

    def calculate(self, consumption_data):
        total_footprint = 0
        for key, value in consumption_data.items():
            if key in self.__emission_factors:
                total_footprint += value * self.__emission_factors[key]

        return round(total_footprint / 1000, 2)