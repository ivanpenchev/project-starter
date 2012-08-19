from django.contrib.auth.models import User

from .page_template import PageTemplate
from .page_element import PageElement
from .page_setting import PageSetting

from django.db import models

class Page(models.Model):
	"""
	Model for the coming-soon pages
	"""

	# One creator
	creator = models.ForeignKey(User)

	# Many elements in the same page
	elements = models.ManyToManyField(PageElement)
	# The page can have many settings
	settings = models.ManyToManyField(PageSetting)
	# It has a template
	template = models.ForeignKey(PageTemplate)

	# Multilanguage support
	languages = models.CharField(max_length=100, default="en")
	# Is the page published?
	published = models.BooleanField(default=False)

	# Automatic timestamp fields
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.creator)

	@classmethod
	def fetch(cls, **kwargs):
		return Page.objects.filter(**kwargs).order_by('-id')

	def get_element(self, identifier):
		if identifier == 'site_name':
			identifier = 1
		if identifier == 'site_slogan':
			identifier = 2

		page_element = self.elements.filter(position=identifier)

		return page_element[0].content if page_element else None

	def get_setting(self, identifier):
		page_setting = self.settings.filter(name=identifier)

		return page_setting[0].value if page_setting else None

	class Meta:
		app_label = 'builder'