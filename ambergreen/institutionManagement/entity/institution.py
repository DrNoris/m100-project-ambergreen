from ambergreen.sharedInfrastructure.entity import Entity

class Institution(Entity):

    def __init__(self, name, address, energy_provider=None, water_provider=None, gas_provider=None, entity_id = None):
        super().__init__(entity_id)
        self.__name = name
        self.__address = address
        self.__energy_provider = energy_provider
        self.__water_provider = water_provider
        self.__gas_provider = gas_provider

    def getId(self):
        return super().getId()

    def getName(self):
        return self.__name

    def getAddress(self):
        return self.__address

    def getEnergyProvider(self):
        return self.__energy_provider

    def getWaterProvider(self):
        return self.__water_provider

    def getGasProvider(self):
        return self.__gas_provider

    def setEnergyProvider(self, energy_provider):
        self.__energy_provider = energy_provider

    def setWaterProvider(self, water_provider):
        self.__water_provider = water_provider

    def setGasProvider(self, gas_provider):
        self.__gas_provider = gas_provider

    def __eq__(self, other):
        if isinstance(other, Institution):
            return (self.getId() == other.getId()) or (self.__name == other.__name and self.__address == other.__address)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"entity_id={self.getId()}, "
            f"name='{self.__name}', "
            f"address='{self.__address}', "
            f"energy_provider='{self.__energy_provider}', "
            f"water_provider='{self.__water_provider}', "
            f"gas_provider='{self.__gas_provider}'"
            f")"
        )

