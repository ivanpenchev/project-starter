from django.db import models

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

	def __unicode__(self):
		return str(self.content)
		
	class Meta:
		app_label = 'builder'