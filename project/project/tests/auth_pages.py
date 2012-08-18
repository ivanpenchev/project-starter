from django.utils import unittest
from django.contrib.auth.models import User
from django.test.client import Client

class AuthPagesTestCase(unittest.TestCase):
    def setUp(self):
        """
            Initialize client to make get and post requests.
        """
        self.client = Client()

    def test_home(self):
        """
            The test should try the response codes for home view using get and post request.
            The first one - using method GET - should return response code 200 success.
            If we use POST method we should be redirected to the same page but this time
            using GET. So the response code will be 302 redirect.
        """
        get_response = self.client.get('/')
        post_response = self.client.post('/')
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_login(self):
        """
            Try the response codes for signing in and whether the user has signed in
            or not after POST request. The first time the user should not be able to sign in.
            After that we create new user and try signing in again. This time of we try to send GET
            request to sign-in it should redirect us.
        """
        login_credentials = {'email':'admin@example.com', 'password':'admin'}
        get_response = self.client.get('/sign-in')
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post('/sign-in', login_credentials)
        self.assertEqual(post_response.status_code, 302)

        User.objects.create_user(username='admin', email='admin@example.com', password='admin')

        post_response = self.client.post('/sign-in', login_credentials)
        self.assertEqual(post_response.status_code, 302)

        get_response = self.client.get('/sign-in')
        self.assertEqual(get_response.status_code, 302)