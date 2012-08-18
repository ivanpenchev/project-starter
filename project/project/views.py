# project/views.py
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.utils import simplejson
from django.core.serializers import json, serialize
from django.template import RequestContext, loader
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
		return self.template_response(request)

class LoginView(BaseView):

    def get(self, request):
		return self.template_response(request, template_name="sign_in.html")