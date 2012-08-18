from django.utils import unittest
from django.test.client import Client

class AuthPagesTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        response = self.client.get('/')
        status = response.status_code
        self.assertEqual(status, 200)