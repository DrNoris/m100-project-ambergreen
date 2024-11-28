import unittest
from institutionUserManagement.validator.institutionUserValidator import InstitutionUserValidator
from institutionUserManagement.entity.institutionUser import InstitutionUser

class TestInstitutionUserValidator(unittest.TestCase):
    def setUp(self):
        """
        Set up the validator and valid test data.
        """
        self.validator = InstitutionUserValidator()
        self.valid_user = InstitutionUser(username="valid_user", password="valid_pass", institution_id=42)

    def test_valid_user(self):
        """
        Test that a valid InstitutionUser passes validation.
        """
        result = self.validator.validate(self.valid_user)
        self.assertTrue(result)

    def test_invalid_type(self):
        """
        Test that a ValueError is raised for invalid entity type.
        """
        with self.assertRaises(ValueError) as context:
            self.validator.validate("Not an InstitutionUser")
        self.assertEqual(str(context.exception), 'Entity is not an instance of InstitutionUser')

    def test_invalid_institution_id(self):
        """
        Test that validation fails for invalid institution IDs.
        """
        invalid_user = InstitutionUser(username="valid_user", password="valid_pass", institution_id=None)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(invalid_user)
        self.assertEqual(str(context.exception), 'Entity id may none or not be integer or bigger than 0')

        invalid_user = InstitutionUser(username="valid_user", password="valid_pass", institution_id=-1)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(invalid_user)
        self.assertEqual(str(context.exception), 'Entity id may none or not be integer or bigger than 0')

    def test_invalid_username(self):
        """
        Test that validation fails for invalid usernames.
        """
        invalid_user = InstitutionUser(username=None, password="valid_pass", institution_id=42)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(invalid_user)
        self.assertEqual(str(context.exception), 'Entity username may none or not be string')

        invalid_user = InstitutionUser(username="", password="valid_pass", institution_id=42)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(invalid_user)
        self.assertEqual(str(context.exception), 'Entity username may none or not be string')

    def test_invalid_password(self):
        """
        Test that validation fails for invalid passwords.
        """
        invalid_user = InstitutionUser(username="valid_user", password=None, institution_id=42)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(invalid_user)
        self.assertEqual(str(context.exception), 'Entity password may none or not be string')

        invalid_user = InstitutionUser(username="valid_user", password="", institution_id=42)
        with self.assertRaises(ValueError) as context:
            self.validator.validate(invalid_user)
        self.assertEqual(str(context.exception), 'Entity password may none or not be string')

if __name__ == "__main__":
    unittest.main()