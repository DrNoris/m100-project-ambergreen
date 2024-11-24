from typing import List

from absl.flags import validator

from institutionManagement.entity.institution import Institution
from institutionManagement.validator.institutionValidator import InstitutionValidator
from sharedInfrastructure.abstractRepository import AbstractRepository


class InstitutionService:
    def __init__(self, repo: AbstractRepository, institutionValidator: InstitutionValidator):
        self.repo = repo
        self.validator = institutionValidator

    def addInstitution(self, institution):
        try:
            self.validator.validate(institution)
            self.repo.add(institution)
        except Exception as e:
            print(e)

    def removeInstitution(self, institution_id : int):
        try:
            self.repo.remove(institution_id)
        except Exception as e:
            print(e)

    def updateInstitution(self, institution: Institution):
        try:
            self.validator.validate(institution)
            self.repo.update(institution)
        except Exception as e:
            print(e)

    def getInstitution(self, institution_id : int):
        try:
            return self.repo.get(institution_id)
        except Exception as e:
            print(e)

    def getInstitutions(self) -> List[Institution]:
        return self.repo.getAll()