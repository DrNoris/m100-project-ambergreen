import unittest

from institutionManagement.entity.institution import Institution
from institutionManagement.validator.institutionValidator import InstitutionValidator


class TestValidator(unittest.TestCase):
    """
        Unit tests for the InstitutionValidator class.
        """

    def setUp(self):
        self.validator = InstitutionValidator()

    def test_validate_valid_institution(self):
        institution = Institution("University of Python", "123 Python St", 1)
        self.assertTrue(self.validator.validate(institution))

    def test_validate_invalid_name_empty(self):
        institution = Institution("", "123 Python St", 1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(institution)
        self.assertEqual(str(context.exception), "Institution name cannot be empty and must be a valid string.")

    def test_validate_invalid_name_whitespace(self):
        institution = Institution("   ", "123 Python St", 1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(institution)
        self.assertEqual(str(context.exception), "Institution name cannot be empty and must be a valid string.")

    def test_validate_invalid_name_not_string(self):
        institution = Institution(12345, "123 Python St", 1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(institution)
        self.assertEqual(str(context.exception), "Institution name cannot be empty and must be a valid string.")

    def test_validate_invalid_address_empty(self):
        institution = Institution("", "University of Python", 1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(institution)
        self.assertEqual(str(context.exception), "Institution name cannot be empty and must be a valid string.")

    def test_validate_invalid_address_whitespace(self):
        institution = Institution("University of Python", " ", 1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(institution)
        self.assertEqual(str(context.exception), "Institution address cannot be empty and must be a valid string.")

    def test_validate_invalid_address_not_string(self):
        institution = Institution("Name", 12345, 1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(institution)
        self.assertEqual(str(context.exception), "Institution address cannot be empty and must be a valid string.")

    def test_validate_invalid_type(self):
        invalid_object = {"id": 1, "name": "University of Python", "address": "123 Python St"}
        with self.assertRaises(TypeError) as context:
            self.validator.validate(invalid_object)
        self.assertEqual(str(context.exception), "Expected Institution, got dict.")


if __name__ == '__main__':
    unittest.main()