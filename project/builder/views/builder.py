from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from project.views import BaseView
from ..models import *

class BuilderView(BaseView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		"""
		Must log in to view this content
		"""
		return super(BuilderView, self).dispatch(*args, **kwargs)


	def get(self, *args, **kwargs):
		request = args[0]

		if 'id' in kwargs:
			page_id = kwargs.get('id')
			page = Page.fetch(id=page_id)

			if page:
				if 'action' in kwargs:
					template_name = 'builder/partials/'+kwargs.get('action')+'.html'
					builder_content = self.template_to_string(request, template_name=template_name, context_data={'page' : page[0]})
					output = { 'builder_content' : builder_content, 'page_id' : page_id }

					if request.is_ajax() and 'json' in kwargs:
						return self.json(output)
					else:
						output['page'] = page[0]
						return self.template_response(request, template_name='builder/main.html', context_data=output)

				return self.one(*args, **kwargs)

		return HttpResponseRedirect('/')

	def post(self, *args, **kwargs):
		if 'id' in kwargs:
			page = Page.fetch(id=kwargs['id'])

			if page:
				if 'action' in kwargs:
					func = getattr(self, kwargs.get('action'))
					return func(*args, **kwargs)

		return HttpResponseRedirect('/')

	def one(self, *args, **kwargs):
		"""
		View the site builder
		"""

		return HttpResponseRedirect(reverse('landing-page', kwargs={'id' : kwargs['id']}))