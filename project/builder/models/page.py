from django.contrib.auth.models import User

from .page_template import PageTemplateModel
from .page_element import PageElementModel

from django.db import models

class PageModel(models.Model):
	"""
	Model for the coming-soon pages
	"""

	# One creator
	creator = models.ForeignKey(User)

	# Many elements in the same page
	elements = models.ManyToManyField(PageElementModel)
	# It has a template
	template = models.ForeignKey(PageTemplateModel)

	# Multilanguage support
	languages = models.CharField(max_length=100, default="en")
	# Is the page published?
	published = models.BooleanField(default=False)

	# Automatic timestamp fields
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.creator)

	class Meta:
		app_label = 'builder'