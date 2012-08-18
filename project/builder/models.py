from django.contrib.auth.models import User

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

class PageElement(models.Model):
	"""
	Model for the coming-soon page elements
	"""

	# Element types
	TYPES = (
		(1, 'Text'),
		(2, 'Image')
	)

	# The content may be null and can contain data depending on element's type
	content = models.TextField(blank=True)

	# Element's type
	element_type = models.PositiveSmallIntegerField(default=1, choices=TYPES)
	# The position of the element on the page
	position = models.CommaSeparatedIntegerField(max_length=100)
	# Multilanguage support
	language = models.CharField(max_length=100, default="en")
	# Whether it is custom (user-created) or syste-created
	custom = models.BooleanField(default=False)

class Template(models.Model):
	"""
	Model for page's templates
	"""

	# Page's background
	background = models.CharField(max_length=200)
	# Central box background
	box_background = models.CharField(max_length=200)
	# Page's text color
	text_color = models.CharField(max_length=20)

	# Whether it is custom (user-created) or syste-created
	custom = models.BooleanField(default=False)