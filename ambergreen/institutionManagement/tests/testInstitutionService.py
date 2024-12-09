from typing import Dict, List
from ambergreen.sharedInfrastructure.abstractRepository import AbstractRepository
import unittest
from ambergreen.institutionManagement.entity.institution import Institution
from ambergreen.institutionManagement.validator.institutionValidator import InstitutionValidator
from ambergreen.institutionManagement.service.institutionService import InstitutionService

class InMemoryRepository(AbstractRepository[Institution]):
    def __init__(self):
        self._store: Dict[int, Institution] = {}
        self._id_counter = 1

    def add(self, institution: Institution) -> Institution:
        institution.id = self._id_counter  # Simulate auto-increment
        self._store[self._id_counter] = institution
        self._id_counter += 1
        return institution

    def remove(self, institution_id: int) -> None:
        if institution_id not in self._store:
            raise KeyError(f"Institution with ID {institution_id} does not exist.")
        del self._store[institution_id]

    def get(self, institution_id: int) -> Institution:
        if institution_id not in self._store:
            raise KeyError(f"Institution with ID {institution_id} does not exist.")
        return self._store[institution_id]

    def update(self, institution: Institution) -> Institution:
        return Institution("", "")

    def getAll(self) -> List[Institution]:
        return list(self._store.values())


class TestInstitutionService(unittest.TestCase):
    def setUp(self):
        # Set up the repository, validator, and service
        self.repo = InMemoryRepository()
        self.validator = InstitutionValidator()
        self.service = InstitutionService(self.repo, self.validator)

    def test_add_institution(self):
        institution = Institution("University of Python", "123 Python St")
        self.service.addInstitution(institution)

        institutions = self.service.getInstitutions()
        self.assertEqual(len(institutions), 1)
        self.assertEqual(institutions[0].getName(), "University of Python")
        self.assertEqual(institutions[0].getAddress(), "123 Python St")

    def test_remove_institution(self):
        institution = Institution("University of Python", "123 Python St")
        added_institution = self.repo.add(institution)  # Add directly via repository for setup
        self.service.removeInstitution(added_institution.id)

        institutions = self.service.getInstitutions()
        self.assertEqual(len(institutions), 0)

    def test_get_institution(self):
        institution = Institution("University of Python", "123 Python St")
        added_institution = self.repo.add(institution)  # Add directly via repository for setup

        retrieved_institution = self.service.getInstitution(added_institution.id)
        self.assertEqual(retrieved_institution.getName(), "University of Python")
        self.assertEqual(retrieved_institution.getAddress(), "123 Python St")

    def test_get_institutions(self):
        self.repo.add(Institution("University of Python", "123 Python St"))
        self.repo.add(Institution("Institute of AI", "456 AI Blvd"))

        institutions = self.service.getInstitutions()
        self.assertEqual(len(institutions), 2)
        self.assertEqual(institutions[0].getName(), "University of Python")
        self.assertEqual(institutions[1].getName(), "Institute of AI")


if __name__ == "__main__":
    unittest.main()


