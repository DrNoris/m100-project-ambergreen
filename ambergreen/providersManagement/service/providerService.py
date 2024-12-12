from typing import List

from ambergreen.providersManagement.entity.provider import Provider
from ambergreen.sharedInfrastructure.abstractRepository import AbstractRepository


class ProviderService:
    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    def addProvider(self, provider):
        try:
            self.repo.add(provider)
        except Exception as e:
            print(e)

    def removeProvider(self, provider_name: str):
        try:
            self.repo.remove(provider_name)
        except Exception as e:
            print(e)

    def updateProvider(self, provider: Provider):
        try:
            self.repo.update(provider)
        except Exception as e:
            print(e)

    def getProvider(self, provider_name: str):
        try:
            return self.repo.get(provider_name)
        except Exception as e:
            print(e)

    def getProviders(self) -> List[Provider]:
        return self.repo.getAll()