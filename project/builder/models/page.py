from django.contrib.auth.models import User

from .template import Template
from .page_element import PageElement

from django.db import models

class Page(models.Model):
	"""
	Model for the coming-soon pages
	"""

	# One creator
	creator = models.ForeignKey(User)

	# Many elements in the same page
	elements = models.ManyToManyField(PageElement)
	# It has a template
	template = models.ForeignKey(Template)

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