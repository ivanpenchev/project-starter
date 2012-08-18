
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from project.views import BaseView

class PageCreate(BaseView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		"""
		Must log in to view this content
		"""
		return super(PageCreate, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		"""
		Return create page response
		"""

		return self.template_response(request)