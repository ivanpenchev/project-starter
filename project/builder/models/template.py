from django.db import models

class Template(models.Model):
	"""
	Model for page's templates
	"""

	# Page's background
	background = models.CharField(max_length=200, default="#fff")
	# Central box background
	box_background = models.CharField(max_length=200, default="#fff")
	# Page's text color
	text_color = models.CharField(max_length=20, default="#000")

	# Whether it is custom (user-created) or syste-created
	custom = models.BooleanField(default=False)
	
	def __unicode__(self):
		return str(self.background)

	class Meta:
		app_label = 'builder'