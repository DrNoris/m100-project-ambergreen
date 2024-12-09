from typing import Dict, List
from ambergreen.sharedInfrastructure.abstractRepository import AbstractRepository
import unittest
from ambergreen.institutionUserManagement.entity.institutionUser import InstitutionUser
from ambergreen.institutionUserManagement.validator.institutionUserValidator import InstitutionUserValidator
from ambergreen.institutionUserManagement.service.InstitutionUserService import InstitutionUserService


class InMemoryRepository(AbstractRepository[InstitutionUser]):
    def __init__(self):
        self._store: Dict[int, InstitutionUser] = {}
        self._id_counter = 1

    def add(self, user: InstitutionUser) -> InstitutionUser:
        self._store[user.getInstitutionId()] = user
        return user

    def remove(self, user: InstitutionUser) -> None:
        if user.getInstitutionId() not in self._store:
            raise KeyError(f"InstitutionUser with ID {user.getInstitutionId()} does not exist.")
        del self._store[user.getInstitutionId()]

    def get(self, user_id: int) -> InstitutionUser:
        if user_id not in self._store:
            raise KeyError(f"InstitutionUser with ID {user_id} does not exist.")
        return self._store[user_id]

    def update(self, user: InstitutionUser) -> InstitutionUser:
        if user.getInstitutionId() not in self._store:
            raise KeyError(f"InstitutionUser with ID {user.getInstitutionId()} does not exist.")
        self._store[user.getInstitutionId()] = user
        return user

    def getAll(self) -> List[InstitutionUser]:
        return list(self._store.values())




class TestInstitutionUserService(unittest.TestCase):
    def setUp(self):
        """
        Set up the repository, validator, and service for testing.
        """
        self.repo = InMemoryRepository()
        self.validator = InstitutionUserValidator()
        self.service = InstitutionUserService(self.repo, self.validator)

        # Sample user
        self.sample_user = InstitutionUser("username1", "password1", 42)

    def test_add_user(self):
        """
        Test adding a valid user.
        """
        self.service.addUser(self.sample_user)
        users = self.service.getUsers()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].getUsername(), "username1")

    def test_remove_user(self):
        """
        Test removing an existing user.
        """
        self.service.addUser(self.sample_user)
        self.service.removeUser(self.sample_user)
        users = self.service.getUsers()
        self.assertEqual(len(users), 0)

    def test_update_user(self):
        """
        Test updating an existing user.
        """
        self.service.addUser(self.sample_user)
        updated_user = InstitutionUser("username1_updated", "password1_updated", 42)
        self.service.updateUser(updated_user)
        user = self.service.getUser(self.sample_user.getInstitutionId())
        self.assertEqual(user.getUsername(), "username1_updated")
        self.assertEqual(user.getPassword(), "password1_updated")

    def test_get_user(self):
        """
        Test retrieving a specific user by institution ID.
        """
        self.service.addUser(self.sample_user)
        user = self.service.getUser(self.sample_user.getInstitutionId())
        self.assertEqual(user.getUsername(), "username1")

    def test_get_users(self):
        """
        Test retrieving all users.
        """
        user2 = InstitutionUser("username2", "password2", 43)
        self.service.addUser(self.sample_user)
        self.service.addUser(user2)
        users = self.service.getUsers()
        self.assertEqual(len(users), 2)
        self.assertIn(self.sample_user, users)
        self.assertIn(user2, users)

    def test_invalid_user(self):
        """
        Test adding an invalid user.
        """
        invalid_user = InstitutionUser(None, None, -1)
        with self.assertRaises(RuntimeError):
            self.service.addUser(invalid_user)


if __name__ == "__main__":
    unittest.main()
