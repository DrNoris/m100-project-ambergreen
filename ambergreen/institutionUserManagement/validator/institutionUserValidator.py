from ambergreen.institutionUserManagement.entity.institutionUser import InstitutionUser
from ambergreen.sharedInfrastructure.validator import Validator


class InstitutionUserValidator(Validator):
    def __init__(self):
        pass

    def validate(self, entity):
        if not isinstance(entity, InstitutionUser):
            raise ValueError('Entity is not an instance of InstitutionUser')

        if entity.getInstitutionId() is None or entity.getInstitutionId() < 0 or not isinstance(entity.getInstitutionId(), int):
            raise ValueError('Entity id may none or not be integer or bigger than 0')

        if entity.getUsername() is None or len(entity.getUsername()) < 0 or not isinstance(entity.getUsername(), str) or entity.getUsername().strip() == '':
            raise ValueError('Entity username may none or not be string')

        if entity.getPassword() is None or len(entity.getPassword()) < 0 or not isinstance(entity.getPassword(), str) or entity.getPassword().strip() == '':
            raise ValueError('Entity password may none or not be string')

        return True