from django import forms

from builder.models import *

class PageCreateForm(forms.Form):
	site_name = forms.CharField(required=True)
	site_slogan = forms.CharField(required=True)

	def save(self, request, obj_page=None):
		if not obj_page:
			obj_page = PageModel()

		# Get the creator
		creator = request.user

		# Create a page element
		page_element = PageElementModel(content='This is a test element.', position=1)
		page_element.save()

		# And a template
		template = PageTemplateModel()
		template.save()

		# Create the page
		obj_page.creator = creator
		obj_page.template = template
		obj_page.save()
		obj_page.elements.add(page_element)

		return obj_page