# project/views.py
from django import http
from django.template import RequestContext, loader
from django.utils import simplejson
from django.views.generic import View
from django.views.generic import TemplateView

class BaseView(View):
    """
    Base django class based view
    """

    def template_response(self, request, template_name, context_data={}):
    	"""Return a HttpResponse by given template name and context data"""

        template = loader.get_template(template_name)
        context = RequestContext(request, context)

        return http.HttpResponse(template.render(context))

    def template_to_string(self, request, template_name, context_data={}):
    	"""Return a template response, rendered to string"""

        template_string = ''
        try:
            template_string = loader.render_to_string(template_name, RequestContext(request, context_data))
        except:
            pass

        return template_string

    def json(self, response_object={}):
    	"""Return a json response"""

        content = json_serialize(response_object)

        return http.HttpResponse(content, mimetype='application/json')

    def invalid_request(self, request):
    	"""Return a bad request"""

        return http.HttpResponseBadRequest()

class LoginView(TemplateView):
    template_name = "login.html"

class TestView(BaseView):

	def get(self, request):
		return self.template_response(request, template_name='test.html')