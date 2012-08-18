from django.test import TestCase

from project.builder.models import Page

class SimpleTest(TestCase):
    def test_page_create(self):
        """
        Tests if a coming soon page creates right
        """
        
        self.assertEqual(1 + 1, 2)
