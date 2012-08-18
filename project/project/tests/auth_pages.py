from django.core.urlresolvers import reverse
from django.utils import unittest
from django.contrib.auth.models import User
from django.test.client import Client

class AuthPagesTestCase(unittest.TestCase):
    def setUp(self):
        """
            Initialize client to make get and post requests and create one user
            for testing purposes.
        """
        self.client = Client()

        self.login_credentials = {'email':'admin@example.com', 'password':'admin'}

    def test_home(self):
        """
            The test should try the response codes for home view using get and post request.
            The first one - using method GET - should return response code 200 success.
            If we use POST method we should be redirected to the same page but this time
            using GET. So the response code will be 302 redirect.
        """
        get_response = self.client.get(reverse('home'))
        post_response = self.client.post(reverse('home'))
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 302)

    def test_login(self):
        """
            Try the response codes for signing in and whether the user has signed in
            or not after POST request. The first time the user should not be able to sign in
            because it won't exists - we'll use our fake(wrong) credentials. Second the we try to sign in
            again but this using rel credentials for the user we created earlier in this class(sgnUp method)
        """
        User.objects.create_user(username='admin', email='admin@example.com', password='admin')
        fake_credentials = {'email':'test@example.com', 'password':'12345'}
        get_response = self.client.get(reverse('sign-in'))
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(reverse('sign-in'), fake_credentials)
        self.assertEqual(post_response.status_code, 302)

        get_response = self.client.get(reverse('sign-in'))
        self.assertEqual(get_response.status_code, 200)

        post_response = self.client.post(reverse('sign-in'), self.login_credentials)
        self.assertEqual(post_response.status_code, 302)

        get_response = self.client.get(reverse('sign-in'))
        self.assertEqual(get_response.status_code, 302)

        self.client.logout()

    def test_logout(self):
        """
            First login the user. After that check whether the user is really logged in or not.
            If  the user is logged in we are going to try the logout view. As soon as we call it,
            it should destroy all user sessions and redirect to sign-in page which means 302 response.
            Finally verify that the user is really logged out by inspecting the client session.
        """
        login_result = self.client.login(username='admin', password='admin')

        self.assertTrue(login_result)
        self.assertIn('_auth_user_id', self.client.session)

        get_response = self.client.get(reverse('logout'))
        self.assertEqual(get_response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)