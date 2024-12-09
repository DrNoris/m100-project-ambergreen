import unittest
from ambergreen.consumptionDataManagement.validator.consumptionDataValidator import ConsumptionDataValidator
from ambergreen.consumptionDataManagement.entity.consumptionData import ConsumptionData


class TestConsumptionDataValidator(unittest.TestCase):
    def setUp(self):
        """
        Set up the validator and valid sample data.
        """
        self.validator = ConsumptionDataValidator()
        self.valid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            energyProvider="Energy Provider",
            gasProvider="Gas Provider",
            waterProvider="Water Provider",
            institutionId=1
        )

    def test_validate_valid_data(self):
        """
        Test that validation passes for valid data.
        """
        result = self.validator.validate(self.valid_data)
        self.assertTrue(result)

    def test_invalid_type(self):
        """
        Test that a TypeError is raised for invalid data types.
        """
        with self.assertRaises(TypeError):
            self.validator.validate("Not a ConsumptionData object")

    def test_invalid_id(self):
        """
        Test that validation fails for invalid or missing IDs.
        """
        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=None
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=-1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

    def test_invalid_water_consumption(self):
        """
        Test that validation fails for invalid water consumption.
        """
        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=None,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=-10.0,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

    def test_invalid_gas_consumption(self):
        """
        Test that validation fails for invalid gas consumption.
        """
        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=None,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=-5.0,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

    def test_invalid_energy_consumption(self):
        """
        Test that validation fails for invalid energy consumption.
        """
        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=None,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=5,
            year=2023,
            energyConsumption=-50.0,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

    def test_invalid_year(self):
        """
        Test that validation fails for invalid years.
        """
        invalid_data = ConsumptionData(
            month=5,
            year=None,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=5,
            year=1899,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

    def test_invalid_month(self):
        """
        Test that validation fails for invalid months.
        """
        invalid_data = ConsumptionData(
            month=None,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=0,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)

        invalid_data = ConsumptionData(
            month=13,
            year=2023,
            energyConsumption=150.5,
            gasConsumption=80.2,
            waterConsumption=50.3,
            institutionId=1
        )
        with self.assertRaises(ValueError):
            self.validator.validate(invalid_data)


if __name__ == "__main__":
    unittest.main()
