from ambergreen.sharedInfrastructure.entity import Entity

class Institution(Entity):

    def __init__(self, name, address,  entity_id = None):
        super().__init__(entity_id)
        self.__name = name
        self.__address = address

    def getId(self):
        return super().getId()

    def getName(self):
        return self.__name

    def getAddress(self):
        return self.__address

    def __eq__(self, other):
        if isinstance(other, Institution):
            return (self.getId() == other.getId()) or (self.__name == other.__name and self.__address == other.__address)


    def __repr__(self):
        return (
            f"entity_id={self.getId()}, "
            f"name='{self.__name}', "
            f"address='{self.__address}'"
        )

