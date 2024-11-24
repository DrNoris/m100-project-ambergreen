import unittest

from psycopg2 import OperationalError

from institutionManagement.repository.institutionDBRepository import InstitutionDBRepository


class TestInstitutionRepository(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        self.database = "m100"
        self.user = "postgres"
        self.password = "postgres"

    def test_connection(self):
        try:
            repository = InstitutionDBRepository(self.host, self.database, self.user, self.password)
            self.repo = repository
            self.assertIsNotNone(repository.connection)
            self.assertIsNotNone(repository.cursor)

            repository.cursor.execute("SELECT 1;")
            result = repository.cursor.fetchone()
            self.assertEqual(result[0], 1)

        except OperationalError as e:
            self.fail(f"Database connection failed: {e}")

    def tearDown(self):
        try:
            self.repo.connection.close()
        except Exception:
            pass

if __name__ == "__main__":
    unittest.main()
