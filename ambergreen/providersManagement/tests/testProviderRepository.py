import unittest

from ambergreen.providersManagement.repository.providersDBRepository import ProviderDBRepository


class TestProviderDBRepository(unittest.TestCase):
    def setUp(self):
        self.repo = ProviderDBRepository("localhost", "m100", "postgres", "postgres")

    def test_connection(self):
        try:
            self.repo.createTable()
            connected = True
        except Exception as e:
            print(f"Connection failed: {e}")
            connected = False

        self.assertTrue(connected)