import unittest
from unittest.mock import MagicMock

from ambergreen.providersManagement.entity.provider import Provider
from ambergreen.providersManagement.service.providerService import ProviderService


class TestProviderService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = ProviderService(self.mock_repo)

    def test_add_provider(self):
        provider = Provider("Provider A", 1.23, "Electricity")
        self.service.addProvider(provider)
        self.mock_repo.add.assert_called_with(provider)

    def test_remove_provider(self):
        self.service.removeProvider("Provider A")
        self.mock_repo.remove.assert_called_with("Provider A")

    def test_update_provider(self):
        provider = Provider("Provider A", 2.34, "Gas")
        self.service.updateProvider(provider)
        self.mock_repo.update.assert_called_with(provider)

    def test_get_provider(self):
        self.mock_repo.get.return_value = Provider("Provider A", 1.23, "Electricity")
        provider = self.service.getProvider("Provider A")
        self.mock_repo.get.assert_called_with("Provider A")
        self.assertEqual(provider.getId(), "Provider A")

    def test_get_providers(self):
        self.mock_repo.getAll.return_value = [
            Provider("Provider A", 1.23, "Electricity"),
            Provider("Provider B", 2.34, "Gas")
        ]
        providers = self.service.getProviders()
        self.mock_repo.getAll.assert_called_once()
        self.assertEqual(len(providers), 2)
        self.assertEqual(providers[0].getId(), "Provider A")
        self.assertEqual(providers[1].getId(), "Provider B")

if __name__ == "__main__":
    unittest.main()