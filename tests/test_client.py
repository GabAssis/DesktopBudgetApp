import unittest
from app.models.client import Client


class TestClient(unittest.TestCase):
    def test_client_creation(self):
        client = Client('Gabriel de Assis', 'gabriel@gmail.com',
                        '488.416.118-12', '11934593949', 'Rua Manoel Salgado, 220')
        self.assertEqual(client.name, 'Gabriel de Assis')
        self.assertEqual(client.email, 'gabriel@gmail.com')
        self.assertEqual(client.document, '488.416.118-12')
        self.assertEqual(client.phone, '11934593949')
        self.assertEqual(client.address, 'Rua Manoel Salgado, 220')

    if __name__ == '__main__':
        unittest.main()
