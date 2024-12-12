from ambergreen.sharedInfrastructure.entity import Entity


class Provider(Entity):

    def __init__(self, provider_name, emission_factor, service_provided):
        super().__init__(provider_name)  # Using provider_name as entity_id
        self.__emission_factor = emission_factor
        self.__service_provided = service_provided

    def getId(self):
        return super().getId()

    def getEmissionFactor(self):
        return self.__emission_factor

    def getServiceProvided(self):
        return self.__service_provided

    def __eq__(self, other):
        if isinstance(other, Provider):
            return self.getId() == other.getId()

    def __repr__(self):
        return (
            f"provider_name='{self.getId()}', "
            f"emission_factor={self.__emission_factor}, "
            f"service_provided='{self.__service_provided}'"
            f")"
        )