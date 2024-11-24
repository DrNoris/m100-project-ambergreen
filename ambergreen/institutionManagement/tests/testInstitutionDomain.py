import unittest

from institutionManagement.entity.institution import Institution


class TestInstitutionDomain(unittest.TestCase):
    """
    Unit tests for the Institution class.
    """
    def test_initialization(self):
        institution = Institution("University of Python", "123 Python St", 1)
        self.assertEqual(institution.getName(), "University of Python")
        self.assertEqual(institution.getAddress(), "123 Python St")
        self.assertIsNotNone(institution)

    def test_equality_by_id(self):
        institution1 = Institution("University of Python", "123 Python St", 1)
        institution2 = Institution("Different Institution", "456 Other St", 1)
        self.assertEqual(institution1, institution2)

    def test_equality_by_name_and_address(self):
        institution1 = Institution("University of Python", "123 Python St", None)
        institution2 = Institution("University of Python", "123 Python St", None)
        self.assertEqual(institution1, institution2)

    def test_inequality(self):
        institution1 = Institution("University of Python", "123 Python St", 1)
        institution2 = Institution("University of Python", "456 Other St", 2)
        self.assertNotEqual(institution1, institution2)

    def test_repr(self):
        institution = Institution("University of Python", "123 Python St", 1)
        expected_repr = "entity_id=1, name='University of Python', address='123 Python St'"
        self.assertEqual(repr(institution), expected_repr)





if __name__ == '__main__':
    unittest.main()