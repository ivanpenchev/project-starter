from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from project.views import BaseView
from ..forms.main import PageCreateForm

class PageCreateView(BaseView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		"""
		Must log in to view this content
		"""
		return super(PageCreateView, self).dispatch(*args, **kwargs)

	def get(self, *args, **kwargs):
		"""
		Return create page response
		"""

		request = args[0]
		context = {
			'form' : PageCreateForm()
		}

		return self.template_response(request, template_name="create_page.html", context_data=context)

	def post(self, *args, **kwargs):
		"""
		Create the page
		"""

		request = args[0]

		if request.method != "POST":
			return HttpResponseRedirect(reverse('page_create'))

		form = PageCreateForm(data=request.POST)
		data = {
			'messages' : {
				'success' : 'The page was successfully created.',
				'error' : 'An error occurred while creating the page.'
			},
			'on_success_redirect' : 'builder_page'
		}

		return self.form_response(request, template_name="create_page.html", form=form, data=data)
