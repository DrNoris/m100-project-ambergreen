from typing import List

from institutionUserManagement.entity.institutionUser import InstitutionUser
from institutionUserManagement.validator.institutionUserValidator import InstitutionUserValidator
from sharedInfrastructure.abstractRepository import AbstractRepository


class InstitutionUserService:
    def __init__(self, repo: AbstractRepository, institutionUserValidator: InstitutionUserValidator):
        self.repo = repo
        self.validator = institutionUserValidator

    def addUser(self, user: InstitutionUser):
        """
        Add a user to the repository.
        Raises RuntimeError if validation or repository operation fails.
        """
        try:
            self.validator.validate(user)
            self.repo.add(user)
        except Exception as e:
            raise RuntimeError(f"Failed to add user: {e}")

    def removeUser(self, user: InstitutionUser):
        """
        Remove a user from the repository.
        Raises RuntimeError if the repository operation fails.
        """
        try:
            self.repo.remove(user)
        except Exception as e:
            raise RuntimeError(f"Failed to remove user: {e}")

    def updateUser(self, user: InstitutionUser):
        """
        Update a user in the repository.
        Raises RuntimeError if validation or repository operation fails.
        """
        try:
            self.validator.validate(user)
            self.repo.update(user)
        except Exception as e:
            raise RuntimeError(f"Failed to update user: {e}")

    def getUser(self, user_id: int) -> InstitutionUser:
        """
        Retrieve a user by institution ID.
        Raises RuntimeError if the repository operation fails.
        """
        try:
            return self.repo.get(user_id)
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve user: {e}")

    def getUsers(self) -> List[InstitutionUser]:
        """
        Retrieve all users from the repository.
        Raises RuntimeError if the repository operation fails.
        """
        try:
            return self.repo.getAll()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve users: {e}")
