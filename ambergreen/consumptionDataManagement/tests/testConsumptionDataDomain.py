import unittest
from consumptionDataManagement.entity.consumptionData import ConsumptionData

class TestConsumptionData(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample ConsumptionData object for reuse in tests.
        """
        self.data = ConsumptionData(
            month=1,
            year=2024,
            energyConsumption=300,
            gasConsumption=100,
            waterConsumption=150,
            energyProvider="Provider A",
            gasProvider="Provider B",
            waterProvider="Provider C",
            institutionId=42
        )

    def test_initialization(self):
        """
        Test that the object initializes correctly.
        """
        self.assertEqual(self.data.getInstitutionId(), 42)
        self.assertEqual(self.data.getMonth(), 1)
        self.assertEqual(self.data.getYear(), 2024)
        self.assertEqual(self.data.getEnergyConsumption(), 300)
        self.assertEqual(self.data.getGasConsumption(), 100)
        self.assertEqual(self.data.getWaterConsumption(), 150)
        self.assertEqual(self.data.getEnergyProvider(), "Provider A")
        self.assertEqual(self.data.getGasProvider(), "Provider B")
        self.assertEqual(self.data.getWaterProvider(), "Provider C")

    def test_equality_same_institution_id(self):
        """
        Test that two objects with the same institution_id are considered equal.
        """
        data2 = ConsumptionData(
            month=2,
            year=2023,
            energyConsumption=400,
            gasConsumption=200,
            waterConsumption=250,
            energyProvider="Another Provider",
            gasProvider="Another Gas Provider",
            waterProvider="Another Water Provider",
            institutionId=42
        )
        self.assertEqual(self.data, data2)

    def test_equality_different_institution_id(self):
        """
        Test that two objects with different institution_ids are not equal.
        """
        data2 = ConsumptionData(
            month=1,
            year=2024,
            energyConsumption=300,
            gasConsumption=100,
            waterConsumption=150,
            energyProvider="Provider A",
            gasProvider="Provider B",
            waterProvider="Provider C",
            institutionId=99
        )
        self.assertNotEqual(self.data, data2)

    def test_getters_with_none_values(self):
        """
        Test that getters handle None values correctly.
        """
        data = ConsumptionData(
            month=1,
            year=2024,
            energyConsumption=300,
            gasConsumption=100,
            waterConsumption=150,
            energyProvider=None,
            gasProvider=None,
            waterProvider=None,
            institutionId=None
        )
        self.assertIsNone(data.getInstitutionId())
        self.assertIsNone(data.getEnergyProvider())
        self.assertIsNone(data.getGasProvider())
        self.assertIsNone(data.getWaterProvider())

if __name__ == "__main__":
    unittest.main()