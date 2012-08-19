# project/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.serializers import json, serialize
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.generic import View

class BaseView(View):
    """
    Base django class based view
    """

    def dispatch(self, *args, **kwargs):
        """
        Dispatch to corresponding method, e.g. GET to get()
        """
        return super(BaseView, self).dispatch(*args, **kwargs)

    def template_response(self, request, template_name="index.html", context_data={}):
        """Return a HttpResponse by given template name and context data"""

        template = loader.get_template(template_name)
        context = RequestContext(request, context_data)

        if not request.is_ajax():
            return HttpResponse(template.render(context))
        else:
            json_params = {'template': self.template_to_string(request, template_name=template_name, context_data=context_data)}
            return self.json(json_params)

    def template_to_string(self, request, template_name="index.html", context_data={}):
        """Return a template response, rendered to string"""

        template_string = ''
        try:
            template_string = loader.render_to_string(template_name, RequestContext(request, context_data))
        except:
            pass

        return template_string

    def json(self, render_object={}):
        """Return a json response"""

        if isinstance(render_object, HttpResponse):
            content = serialize('json', render_object)
        else:
            content = simplejson.dumps(
                render_object, indent=2, cls=json.DjangoJSONEncoder,
                ensure_ascii=False
            )

        return HttpResponse(content, mimetype='application/json')

    def form_response(self, request, template_name, form, data={}):
        """Handle form responses"""

        output = {}
        if form.is_valid():
            try:
                output = {
                    'success' : data['messages']['success'] if 'success' in data['messages'] else True,
                    'db_object' : form.save(request, data['db_object'] if 'db_object' in data else None)
                }
            except Exception:
                output = {
                    'success' : False,
                    'form' : form,
                    'custom_errors' : { data['messages']['error'] } if 'error' in data['messages'] else False
                }
        else:
            output = {
                'success' : False,
                'form' : form,
                'errors' : form.errors
            }

        if request.is_ajax():
            return self.json(output)
        else:
            if output['success']:
                db_object = output['db_object']

                if 'on_success_redirect' in data:
                    return HttpResponseRedirect(reverse(data['on_success_redirect'], kwargs={'id' : db_object.id}))
            else:
                return self.template_response(request, template_name=template_name, context_data=output)


class HomeView(BaseView):

    def get(self, request):
        """
            Render appropriate template when get request to HomeView is received
        """
        return self.template_response(request)

    def post(self, request):
        """
            If the received request type is post redirect to the home page
        """
        return HttpResponseRedirect(reverse('home'))


class SignupView(BaseView):

    def get(self, request):
        """
            Render sign up form
        """
        if not request.user.is_authenticated():
            return self.template_response(request, template_name='sign_up.html')
        else:
            return HttpResponseRedirect(reverse('home'))

    def post(self, request):
        """
            Try to create new user in the database
        """
        if not request.user.is_authenticated():
            post_data = request.POST

            username = post_data['fname']+post_data['lname']
            user = User.objects.create_user(username.lower(), post_data['email'], post_data['password'])

            user.first_name = post_data['fname']
            user.last_name = post_data['lname']
            user.save()

            return HttpResponseRedirect(reverse('sign-in'))
        else:
            return HttpResponseRedirect(reverse('home'))


class LoginView(BaseView):

    def get(self, request):
        """
            Just render and return the login form template
        """
        if not request.user.is_authenticated():
            return self.template_response(request, template_name="sign_in.html")
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

            if post_data:
                user = authenticate(email=post_data['email'], password=post_data['password'])

                if user is not None:
                    request.session['user'] = user

                    if user.is_authenticated():
                        login(request, user)

                        return HttpResponseRedirect(reverse('dashboard'))
        else:
            return HttpResponseRedirect(reverse('dashboard'))

        return HttpResponseRedirect(reverse('sign-in'))


class LostPasswordView(BaseView):

    def get(self, request):
        if not request.user.is_authenticated():
            return self.template_response(request, 'password_lost.html')
        else:
            return HttpResponseRedirect(reverse('sign-in'))

    def post(self, request):
        pass


class DashboardView(BaseView):

    def get(self, request):
        return self.template_response(request, 'dashboard.html')


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
