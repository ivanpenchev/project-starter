from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from project.views import BaseView
from ..models import *
from ..forms.main import PageCreateForm

class PageView(BaseView):
	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		"""
		Must log in to view this content
		"""
		return super(PageView, self).dispatch(*args, **kwargs)

	def get(self, *args, **kwargs):
		if 'action' in kwargs:
			func = getattr(self, kwargs.get('action'))
			return func(*args, **kwargs)

		return self.all(*args, **kwargs)

	def post(self, *args, **kwargs):
		return self.get(*args, **kwargs)

	def all(self, *args, **kwargs):
		"""
		Return a list of all user's pages
		"""

		request = args[0]
		context = { 'user_pages_list' : Page.fetch(creator=request.user) }

		if request.is_ajax():
			return self.json(context)
		else:
			return self.template_response(request, template_name='page/all.html', context_data=context)

	def create(self, *args, **kwargs):
		request = args[0]

		if request.method == "GET":
			"""
			Return create page response
			"""

			context = { 'form' : PageCreateForm() }

			return self.template_response(request, template_name="page/create.html", context_data=context)
		else:
			if request.method == "POST":
				"""
				Create the page
				"""
			
				form = PageCreateForm(data=request.POST)
				data = {
					'messages' : {
						'success' : 'The page was successfully created.',
						'error' : 'An error occurred while creating the page.'
					},
					'on_success_redirect' : 'builder-page'
				}

				return self.form_response(request, template_name="page/create.html", form=form, data=data)

		return HttpResponseRedirect(reverse('page-create'))

	def delete(self, *args, **kwargs):
		request = args[0]

		if request.method == "GET" and 'id' in kwargs:
			page_id = kwargs.get('id')

			page = Page.objects.filter(id=page_id)

			if page:
				page.delete()

		return HttpResponseRedirect(reverse('page-all'))
