from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from project.views import BaseView

class BuilderView(BaseView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		"""
		Must log in to view this content
		"""
		return super(BuilderView, self).dispatch(*args, **kwargs)

	def get(self, *args, **kwargs):
		"""
		Return create page response
		"""

		if 'id' in kwargs:
			return self.json({'id' : kwargs['id']})
		