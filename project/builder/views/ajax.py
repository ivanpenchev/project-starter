from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from project.views import BaseView
from ..models import *

class AjaxView(BaseView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		"""
		Must log in to view this AJAX content
		"""
		return super(AjaxView, self).dispatch(*args, **kwargs)


	def get(self, *args, **kwargs):
		request = args[0]
		if not request.is_ajax():
			return HttpResponseBadRequest()

		if 'action' in kwargs:
			func = getattr(self, kwargs.get('action'))
			return func(*args, **kwargs)

		return HttpResponse('')

	def post(self, *args, **kwargs):
		return self.get(*args, **kwargs)

	def save_element(self, *args, **kwargs):
		"""
		Save element
		"""

		request = args[0]
		output = { 'success' : False }

		page_id = request.POST.get('page_id')
		position = request.POST.get('position')
		content = request.POST.get('content')

		page = Page.fetch(id=page_id)

		if page:
			element = page[0].elements.filter(position=position)

			if element:
				element = element[0]
				element.content = content
				element.save()

				output = { 'success' : True }

		return self.json(output)