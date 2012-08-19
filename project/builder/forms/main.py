from django import forms

from builder.models import *
from project.views import BaseView

class PageCreateForm(forms.Form):
	site_url = forms.URLField(label='Your site\'s URL', initial='http://', required=True)
	site_name = forms.CharField(required=True)
	site_slogan = forms.CharField(required=True)

	def save(self, request, obj_page=None):
		if not obj_page:
			obj_page = Page()

		# Get the creator
		creator = request.user

		# And a template
		template = PageTemplate()
		template.save()

		# Create the page
		obj_page.creator = creator
		obj_page.template = template
		obj_page.save()

		# Create a page element
		page_element = PageElement(content=self.cleaned_data.get('site_name'), position=1)
		page_element.save()
		obj_page.elements.add(page_element)

		# Create a another page element
		page_element = PageElement(content=self.cleaned_data.get('site_slogan'), position=2)
		page_element.save()
		obj_page.elements.add(page_element)

		# Create a page element
		confirmation_email = BaseView().template_to_string(request, template_name='confirmation_email.html')
		page_setting = PageSetting(name='email', value=confirmation_email)
		page_setting.save()
		page_setting = PageSetting(name='site_url', value=self.cleaned_data.get('site_url'))
		page_setting.save()
		obj_page.settings.add(page_setting)

		return obj_page