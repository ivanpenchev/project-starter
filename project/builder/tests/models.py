from django.test import TestCase

from django.contrib.auth.models import User
from builder.models import *

class ModelsTestCase(TestCase):
	def setUp(self):
		"""
		Firstly, setup a user which will be used for testing
		"""

		user = User.objects.create_user(username='unittest', email='unittest@example.com', password='unittest')
		user.first_name = 'UnitTest'
		user.save()

	def test_page_create(self):
		"""
		Tests if a coming soon page creates right
		"""

		# Get the creator
		creator = User.objects.filter(username='unittest')[0]

		# Create a page element
		page_element = PageElement(content='This is a test element.', position=1)
		page_element.save()

		# And a template
		template = Template()
		template.save()

		# Create the page
		create_page = Page(creator=creator, template=template)
		create_page.save()
		create_page.elements.add(page_element)

		# Test it!
		page = Page.objects.filter(id=1)[0];
		self.assertEqual(page.creator.username, 'unittest')
		self.assertEqual(page.elements.all()[0].content, 'This is a test element.')
		self.assertEqual(page.template.text_color, '#000')
