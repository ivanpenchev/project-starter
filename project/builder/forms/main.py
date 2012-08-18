from django import forms

from builder.models import *

class PageCreateForm(forms.Form):
	site_name = forms.CharField(required=True)
	site_slogan = forms.CharField(required=True)

	def save(self, request, obj_page=None):
		if not obj_page:
			obj_page = Page()

		# Get the creator
		creator = request.user

		# Create a page element
		page_element = PageElement(content='This is a test element.', position=1)
		page_element.save()

		# Create a page element
		page_setting = PageSetting(name='email', value='This is the email.')
		page_setting.save()

		# And a template
		template = PageTemplate()
		template.save()

		# Create the page
		obj_page.creator = creator
		obj_page.template = template
		obj_page.save()
		
		obj_page.elements.add(page_element)
		obj_page.settings.add(page_setting)

		return obj_page