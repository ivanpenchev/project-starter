# project/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.utils import simplejson
from django.core.serializers import json, serialize
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.generic import TemplateView

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

        return HttpResponse(template.render(context))

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

    def form_errors(self, form):
        """Get form errors and return them in a json response"""

        output_dict = {'success' : 'false'}

        dictionary = {}
        for element in form.errors.iteritems():
            dictionary.update(
                {
                    element[0] : unicode(element[1])
                }
            )

        output_dict.update({'errors': dictionary})

        return self.json(output_dict)


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
        return HttpResponseRedirect('/')


class SignupView(BaseView):

    def get(self, request):
        """
            Render sign up form
        """
        if not request.user.is_authenticated():
            return self.template_response(request, template_name='sign_up.html')
        else:
            return HttpResponseRedirect('/')

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

            return HttpResponseRedirect('/sign-in')
        else:
            return HttpResponseRedirect('/')


class LoginView(BaseView):

    def get(self, request):
        """
            Just render and return the login form template
        """
        if not request.user.is_authenticated():
            return self.template_response(request, template_name="sign_in.html")
        else:
            return HttpResponseRedirect('/dashboard')

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

                        return HttpResponseRedirect('/dashboard')
        else:
            return HttpResponseRedirect('dashboard')

        return HttpResponseRedirect('/sign-in')


class ChangePasswordView(BaseView):

    def get(self, request):
        return self.template_response(request, 'password_change.html')

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
        return HttpResponseRedirect('/sign-in')
