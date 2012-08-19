# project/auth.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from project.forms.sign_in import SignInForm
from project.forms.sign_up import SignUpForm
from project.libs.github import GitHub
from project.views import BaseView

import string
import random

class SignupView(BaseView):

    def get(self, request):
        """
            Render sign up form
        """
        if not request.user.is_authenticated():
            context = {
                'form' : SignUpForm()
            }
            return self.template_response(request, template_name='sign_up.html', context_data=context)
        else:
            return HttpResponseRedirect(reverse('home'))

    def post(self, request):
        """
            Try to create new user in the database
        """
        if not request.user.is_authenticated():
            post_data = request.POST
            signup_form = SignUpForm(post_data)

            if signup_form.is_valid():
                random_string_chars = string.ascii_letters + string.digits
                random_string = ''.join(random.choice(random_string_chars) for x in range(5))
                username = post_data['fname']+post_data['lname']+'_'+random_string
                user = User.objects.create_user(username.lower(), post_data['email'], post_data['password'])

                user.first_name = post_data['fname']
                user.last_name = post_data['lname']
                user.save()

                return HttpResponseRedirect(reverse('sign-in'))
            else:
                context = {
                    'form' : signup_form,
                    'errors' : signup_form.errors
                }
                return self.template_response(request, 'sign_up.html', context_data=context)
        else:
            return HttpResponseRedirect(reverse('home'))

class LoginView(BaseView):
    authenticate_method = 'django'
    third_party_confirm = False

    def dispatch(self, *args, **kwargs):
        """
            Process kwargs data in order to retrieve the requested
            authentication method and heck whether the request for
            third-party authorization has been confirmed or not.
        """
        if 'type' in kwargs and kwargs.get('type', '') == 'github':
            self.authenticate_method = kwargs.get('type', '')
        self.third_party_confirm = kwargs.get('confirm', False) if 'confirm' in kwargs else False

        kwargs.clear()
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
            If the requested authenticate_method is 'django' simply render
            the login form and return it back to the browser.
            However if  the requested authenticate method requires
            third-party authorization, call the corresponding method
            for the specific account type (e.g. github)
            and probably redirect the user in order to allow our application to
            retrieve his data.
        """
        if not request.user.is_authenticated():
            if self.authenticate_method == 'django':
                context = {
                    'form': SignInForm()
                }
                return self.template_response(request, template_name="sign_in.html", context_data=context)
            else:
                if self.authenticate_method == 'github':
                    return self.auth_github()
                else:
                    raise NotImplemented('')
        else:
            return HttpResponseRedirect(reverse('dashboard'))

    def post(self, request):
        """
            On received POST request try to authenticate the user if there is any data received,
            otherwise, in case there isn't any data or the provided email and password aren't correct,
            redirect to the login page and let the user try again.
        """
        if not request.user.is_authenticated():
            post_data = request.POST
            signin_form = SignInForm(post_data)

            if signin_form.is_valid():

                user = authenticate(email=post_data['email'], password=post_data['password'])

                if user is not None:
                    request.session['user'] = user

                    if user.is_authenticated():
                        login(request, user)

                        return HttpResponseRedirect(reverse('dashboard'))

                return HttpResponseRedirect(reverse('sign-in'))
            else:
                context = {
                    'form' : signin_form,
                    'errors' : signin_form.errors
                }
                return self.template_response(request, 'sign_in.html', context_data=context)
        else:
            return HttpResponseRedirect(reverse('dashboard'))

    def auth_github(self):
        """
            Check whether the authorization request has been confirmed or not.
            If it is not, just redirect the user to his GitHub account in order
            ask him to allow our app to retrieve profile data.
            If this is request confirmation ... use the received access token and
            do something with it to receive needed data.
        """
        github = GitHub()
        if not self.third_party_confirm:
            authorization_url = github.authorize_url(self.request)
            self.request.session['github_state'] = github.state
            return HttpResponseRedirect(authorization_url)
        else:
            state = self.request.GET['state']
            if state == self.request.session['github_state']:
                github.code = self.request.GET['code']
                github.retrieve_token()
                user = github.retrieve_user()
                user_exists = User.objects.filter(email=user['email']).exists()
                if not user_exists:
                    random_password = User.objects.make_random_password(10)
                    user = User.objects.create_user(
                        username=user['login'], email=user['email'], password=random_password
                    )
                    send_mail('ProjectStarter password',
                        'You have successfully signed up for ProjectStarter' +
                        ' using your GitHub account. When you try to login please use' +
                        ' your email address and this random generated password:\n\n\n'+random_password+
                        ' \n\n\n You should better change your password as soon as you log in.\n\n\n'+
                        ' Thank you!',
                        'admin@intrest.in', [user.email], fail_silently=False)

                    user = authenticate(email=user.email, password=random_password)
                    login(self.request, user)
                    return redirect('dashboard')
                else:
                    return redirect('sign-in')
            else:
                raise Exception('Invalid state')

class LostPasswordView(BaseView):

    def get(self, request):
        if not request.user.is_authenticated():
            return self.template_response(request, 'password_lost.html')
        else:
            return HttpResponseRedirect(reverse('sign-in'))

    def post(self, request):
        """
        Generate random password, update the user record by the provided email address
        and send the newly generated password via email to the user.
        """
        pass


class LogoutView(BaseView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
            Simple method to logout the current user when the appropriate
            request is being received.
        """
        logout(request)
        return HttpResponseRedirect(reverse('sign-in'))