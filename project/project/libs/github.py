import random
import string
import urllib
from django.core.urlresolvers import reverse
import requests

class GitHub:
    """
        Very simple python implementation of the GitHub v3 API

        ----------------------------------------------------------------
        code - temporary code which is being received after authorization
        state - used to protect against cross-site request forgery attacks
        access_token - the access token received from GitHub
        ----------------------------------------------------------------

        For further reference: http://developer.github.com/v3/oauth/
    """
    code = None
    state = None
    access_token = False

    def __init__(self, state=False, code=False):
        self.state = state
        self.code = code

    def authorize_url(self, request):
        """
            Return authorization url along with all needed data
        """
        auth_url = 'https://github.com/login/oauth/authorize?'
        self.state = ''.join(random.choice(string.ascii_letters+string.digits) for x in range(7))
        site_url = 'http://'+request.environ['HTTP_HOST']
        params = {
            'client_id' : '117567e79e862c0cede3',
            'redirect_uri' : site_url+reverse('sign-in-confirm', kwargs={'type':'github'}),
            'state' : self.state
        }
        auth_url += urllib.urlencode(params)
        return auth_url

    def retrieve_token(self):
        """
            Retrieve access token form github using previously exchanged
            code and state. Access token is used to later retrieve user profile
            info.
        """
        url = 'https://github.com/login/oauth/access_token'
        params = {
            'client_id' : '117567e79e862c0cede3',
            'client_secret' : '4c2c84c1a151b74692c118c6d72f116b06e2d0cc',
            'code' : self.code,
            'state' : self.state
        }
        headers = {
            'Accept' : 'application/json'
        }
        response = requests.post(url, data=params, headers=headers).json

        if 'error' in response:
            raise Exception('Invalid request: '+response['error'])

        self.access_token = response['access_token']
        self.token_type = response['token_type']

        return self.access_token, self.token_type

    def retrieve_user(self):
        """
            Retrieve all public user data. Access token is requirement.
            It should be retrieved earlier using `retrieve_token` method.
        """
        if self.access_token:
            url = 'https://api.github.com/user?access_token='+self.access_token
            headers = dict(Accepts='application/json')
            response = requests.get(url, headers=headers).json
            return response
        else:
            raise Exception('No access token. First you should retrieve it using retrieve_token method.')