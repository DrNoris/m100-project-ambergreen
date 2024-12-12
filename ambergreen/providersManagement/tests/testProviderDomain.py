import unittest

from ambergreen.providersManagement.entity.provider import Provider


class TestProvider(unittest.TestCase):
    def test_provider_creation(self):
        provider = Provider("Provider A", 1.23, "Electricity")
        self.assertEqual(provider.getId(), "Provider A")
        self.assertEqual(provider.getEmissionFactor(), 1.23)
        self.assertEqual(provider.getServiceProvided(), "Electricity")