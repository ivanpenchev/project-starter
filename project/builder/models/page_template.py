from django.db import models

class PageTemplate(models.Model):
	"""
	Model for page's templates
	"""

	# Template's name
	name = models.CharField(max_length=200)

	# Page's background
	background = models.CharField(max_length=200, default="#fff")
	# Central box background
	box_background = models.CharField(max_length=200, default="#fff")
	# Page's text color
	text_color = models.CharField(max_length=20, default="#000")
	# Page's css
	css = models.TextField(blank=True)

	# Whether it is custom (user-created) or system-created
	custom = models.BooleanField(default=False)
	
	def __unicode__(self):
		return str(self.name)

	@classmethod
	def add_default_templates(cls, **kwargs):
		themes = [
			['theme_1', '#fff', '#fff', '#000'],
			['theme_2', '#000', '#fff', '#000'],
			['theme_3', '#000', '#000', '#fff']
		]

		for theme in themes:
			if PageTemplate.exists(name=theme[0]):
				continue

			template = PageTemplate()

			template.name = theme[0]
			template.background = theme[1]
			template.box_background = theme[2]
			template.text_color = theme[3]

			template.save()

	@classmethod
	def exists(cls, **kwargs):
		template = PageTemplate.objects.filter(**kwargs)

		if template:
			return True

		return False

	@classmethod
	def get_template(cls, **kwargs):
		if PageTemplate.exists(**kwargs):
			return PageTemplate.objects.filter(**kwargs)[0]

		return False

	class Meta:
		app_label = 'builder'