import unittest
from institutionUserManagement.entity.institutionUser import InstitutionUser

class TestInstitutionUser(unittest.TestCase):
    def setUp(self):
        """
        Set up a sample InstitutionUser for reuse in tests.
        """
        self.user1 = InstitutionUser("user1", "password1", 42)
        self.user2 = InstitutionUser("user2", "password2", 43)
        self.user3 = InstitutionUser("user1", "password3", 44)

    def test_initialization(self):
        """
        Test that the InstitutionUser object initializes correctly.
        """
        self.assertEqual(self.user1.getUsername(), "user1")
        self.assertEqual(self.user1.getPassword(), "password1")
        self.assertEqual(self.user1.getInstitutionId(), 42)

    def test_equality_by_id(self):
        """
        Test equality based on institution ID.
        """
        user_with_same_id = InstitutionUser("another_user", "password", 42)
        self.assertEqual(self.user1, user_with_same_id)

    def test_equality_by_username(self):
        """
        Test equality based on username.
        """
        self.assertEqual(self.user1, self.user3)

    def test_inequality(self):
        """
        Test that users with different IDs and usernames are not equal.
        """
        self.assertNotEqual(self.user1, self.user2)

    def test_invalid_comparison(self):
        """
        Test that comparison with an invalid type returns False.
        """
        self.assertNotEqual(self.user1, "Not a user")

    def test_password_is_private(self):
        """
        Test that the password is not directly accessible.
        """
        with self.assertRaises(AttributeError):
            self.user1.__password

if __name__ == "__main__":
    unittest.main()
