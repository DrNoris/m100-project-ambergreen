from ambergreen.sharedInfrastructure.entity import Entity


class InstitutionUser(Entity):

    def __init__(self, username, password, institution_id):
        super().__init__(institution_id)
        self.__username = username
        self.__password = password

    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def getInstitutionId(self):
        return super().getId()

    def __eq__(self, other):
        if isinstance(other, InstitutionUser):
            return self.getId() == other.getId() or self.__username == other.getUsername()
        return False

