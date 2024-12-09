from ambergreen.institutionManagement.entity.institution import Institution
from ambergreen.sharedInfrastructure.validator import Validator


class InstitutionValidator(Validator):
    """
    A validator that checks for
     Id to be positive,
     Name to have more than 0 characters that are not space,
     Name to be string,
     Address to have more than 0 characters that are not space,
     Address to be string,
    """
    def __init__(self):
        pass

    def validate(self, institution):
        if not isinstance(institution, Institution):
            raise TypeError(f"Expected Institution, got {type(institution).__name__}.")

        if not institution.getName() or not isinstance(institution.getName(), str) or len(institution.getName().strip()) == 0:
            raise ValueError("Institution name cannot be empty and must be a valid string.")

        if not institution.getAddress() or not isinstance(institution.getAddress(), str) or len(institution.getAddress().strip()) == 0:
            raise ValueError("Institution address cannot be empty and must be a valid string.")

        return True
