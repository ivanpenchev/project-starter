from django.db import models

class PageSetting(models.Model):
	"""
	Model for the coming-soon page settings
	"""

	# Setting's name
	name = models.CharField(max_length=100)
	# Setting's content
	value = models.TextField()

	# Whether it is custom (user-created) or system-created
	custom = models.BooleanField(default=False)

	def __unicode__(self):
		return str(self.name)
		
	class Meta:
		app_label = 'builder'